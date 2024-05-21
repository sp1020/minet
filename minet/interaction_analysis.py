"""
Interaction Analysis Module

This module evaluates the pairwise interactions of microbes from microbial feature tables. 
It performs co-occurrence analysis, qualitative assessment of co-occurring microbes, and inference of interaction directionality.
"""

import argparse
import logging

import psutil
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.stats import pearsonr
from minet import utility, fdr, cooccurrence, preprocess

# Create a logger
logger = logging.getLogger(__name__)

# Arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-i', dest='input', type=str,
                    help='Input microbial feature table')
parser.add_argument('-o', dest='output', type=str,
                    help='Output interaction analysis result file')
parser.add_argument('--depth', dest='depth', type=int, default=10000,
                    help='Per sample read depth cutoff')
parser.add_argument('--prevalence', dest='prevalence', type=float, default=0.1,
                    help='Per ASV prevalence cutoff')
parser.add_argument('--no-preprocess', dest='no_preprocess', action='store_true', default=False,             
                    help='User this flag for preprocessed input data')


class Analyzer:
    """
    Manages statistical interactions of microbial features from the input microbial feature table.
    """

    def __init__(self):
        """
        Initializes the analysis class
        """
        pass

    def load_feature_table(self, filename, depth=10000, prevalence=0.1, preprocessing=True):
        """
        Loads data from the microbial feature table 
        """
        self.asv_table = pd.read_csv(filename, sep='\t', header=0, index_col=0)
        print(self.asv_table.shape)

        if preprocessing:
            pr = preprocess.Preprocessor(self.asv_table)
            pr.undersampling_by_depth(depth)
            pr.filter_by_prevalence(prevalence)

            self.asv_table = pr.table
            print(self.asv_table.shape)

    def evaluate_feature_association(self, output):
        """
        Evaluate the interactions for all microbial interactions 
        """
        self.output = output

        ix_list = self.asv_table.index.values

        job_list = []
        cnt = 1
        for i, ix1 in enumerate(ix_list):
            for j, ix2 in enumerate(ix_list):
                if i > j:
                    job_list.append([ix1, ix2,
                                     self.asv_table.loc[ix1, :].values,
                                     self.asv_table.loc[ix2, :].values, cnt])
                    cnt += 1
        print('Number of jobs:', len(job_list))

        nthreads = int(psutil.cpu_count())
        jman = utility.Manager(job_permutation, nthreads)
        jman.fill_jobs(job_list)

        res = jman.analyze_result()

        # False discovery rate calculation
        df = pd.DataFrame(res, columns=['Feature1', 'Feature2',
                                        'N12', 'N1', 'N2', 'LogOddsRatio', 'Rho',
                                        'P-value(FisherExact)', 'P-value(Pearson)',
                                        'LogRatio12', 'LogRatio21',
                                        'P-value(12)', 'P-value(21)'])

        f = fdr.FDR()
        df = f.calc(df, pvalue_index='P-value(FisherExact)')[0]
        df.rename(
            columns={'Adjusted-P': 'Adjusted-P(FisherExact)'}, inplace=True)
        df.drop(columns=['Significance'], inplace=True)
        df = f.calc(df, pvalue_index='P-value(Pearson)')[0]
        df.rename(columns={'Adjusted-P': 'Adjusted-P(Pearson)'}, inplace=True)
        df.drop(columns=['Significance'], inplace=True)
        df.to_csv(self.output, sep='\t')


def job_permutation(q_job, q_result):
    """
    Executes permutation tests in multi-thread modes
    """
    while True:
        j = q_job.get()

        if j['type'] == 'JOB':
            ft1 = j['value'][0]
            ft2 = j['value'][1]
            v1 = j['value'][2]
            v2 = j['value'][3]
            cnt = j['value'][4]
            if cnt % 100 == 0:
                print(cnt)

            oddsratio, pv_fs = cooccurrence.coocurrence(v1, v2)
            if oddsratio == 1:
                log_oddsratio = 0
            else:
                log_oddsratio = np.log2(oddsratio)

            nz1 = set(np.nonzero(v1)[0])
            nz2 = set(np.nonzero(v2)[0])
            ci = list(nz1.intersection(nz2))

            v1_nz = np.log(v1[ci])
            v2_nz = np.log(v2[ci])

            if len(ci) <= 5:
                rho = 0
                pv_ps = 1.0
            else:
                sd1 = np.std(v1_nz)
                sd2 = np.std(v2_nz)

                if sd1 == 0 or sd2 == 0:
                    rho = 0
                    pv_ps = 1.
                else:
                    rho, pv_ps = pearsonr(v1_nz, v2_nz)

            # Directionality accessment
            bv1 = np.array(v1, dtype=bool)
            bv2 = np.array(v2, dtype=bool)

            ct_ori = contingency_table(bv1, bv2)
            lr_ori12, lr_ori21 = ct_info(ct_ori)

            rv1 = np.copy(bv1)
            rv2 = np.copy(bv2)

            rs = []
            for i in range(999):
                np.random.shuffle(rv2)

                ct = contingency_table(rv1, rv2)
                lr12, lr21 = ct_info(ct)
                rs.append([lr12, lr21])
            rs = np.array(rs)

            p12 = permut_pvalue(lr_ori12, rs[:, 0])
            p21 = permut_pvalue(lr_ori21, rs[:, 1])

            # Report results
            q_result.put([ft1, ft2, len(ci), len(nz1), len(
                nz2), log_oddsratio, rho, pv_fs, pv_ps,
                lr_ori12, lr_ori21, p12, p21])

        try:
            if j['type'] == 'CONTROL':
                if j['value'] == 'END':
                    break
        except:
            pass


def contingency_table(a, b):
    """
    Creates a contingency table from two presence/absence vectors
    """

    rows = 1 - a
    cols = 1 - b

    ct = np.zeros((2, 2), dtype=float)

    np.add.at(ct, (rows, cols), 1)
    return ct


def ct_info(ct):
    """
    Claculates log odds ratio using the contingency table 
    """
    # pseudo count
    ct += 0.01

    # calculate statistics
    ro21 = np.log2(ct[0, 0]/ct[0, 1])
    ro12 = np.log2(ct[0, 0]/ct[1, 0])
    return (ro12, ro21)


def permut_pvalue(val, vs):
    """
    Calculates the p-value for an input value (val) based on  the results of the permutation tests.
    """
    if val > 0:
        cnt = np.sum(vs > val)
    else:
        cnt = np.sum(vs < val)
    return (cnt + 1) / (len(vs) + 1)
