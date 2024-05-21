"""
Network File Handling Module 

This module parses the association analysis results and creates a microbial interaction network.
"""

import argparse
import logging

import pandas as pd

from minet.cytoscape import CytoscapeXGMML

# Create a logger
logger = logging.getLogger(__name__)

# Arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-i', dest='input', type=str,
                    help='Input result file')
parser.add_argument('-o', dest='output', type=str, default='network.xml',
                    help='Output network file (default: %(default)s)')
parser.add_argument('--fdr-cooccurrence', dest='fdr_co', default=0.05, type=float,
                    help='FDR of coocurrence analysis (default: %(default)s)')
parser.add_argument('--cooccurrence-type', dest='co_type', default='positive', type=str,
                    help='Association type (default: %(default)s)')

parser.add_argument('--fdr-quantitative', dest='fdr_qt', default=0.05, type=float,
                    help='FDR of quantitative analysis (Pearson\'s correlation) (default: %(default)s)')
parser.add_argument('--quantitative-type', dest='qt_type', default='positive', type=str,
                    help='Association type (default: %(default)s)')

parser.add_argument('--directionality-p-value', dest='pval_dir', default=0.05, type=float,
                    help='Association type (default: %(default)s)')


class Network:
    """
    Network analysis class
    """

    def __init__(self) -> None:
        """
        Initializes the network analysis object.
        """
        self.nodes = {}
        self.edges = {}

    def load_interaction_results(self, filename, fdr_co=0.05, fdr_qt=0.05, co_type='positive', qt_type='positive', pval_dir=0.05):
        """
        Loads interaction results and filters interactions
        """
        association = pd.read_csv(filename, sep='\t')
        idx = association.index[(association['Adjusted-P(Pearson)'] < fdr_qt)
                                & (association['Adjusted-P(FisherExact)'] < fdr_co)]
        association = association.loc[idx, :]

        if co_type == 'positive':
            idx = association.index[association['LogOddsRatio'] > 0]
            association = association.loc[idx, :]
        elif co_type == 'negative':
            idx = association.index[association['LogOddsRatio'] < 0]
            association = association.loc[idx, :]

        if qt_type == 'positive':
            idx = association.index[association['Rho'] > 0]
            association = association.loc[idx, :]
        elif qt_type == 'negative':
            idx = association.index[association['Rho'] < 0]
            association = association.loc[idx, :]

        for id, row in association.iterrows():
            ft1 = row['Feature1']
            ft2 = row['Feature2']

            self.nodes[ft1] = {'name': ft1}
            self.nodes[ft2] = {'name': ft2}

            if row['P-value(12)'] < pval_dir:
                e = [ft1, ft2]
                self.edges[tuple(e)] = {'Rho': row['Rho'],
                                        'LogOddsRatio': row['LogOddsRatio']}
            if row['P-value(21)'] < pval_dir:
                e = [ft2, ft1]
                self.edges[tuple(e)] = {'Rho': row['Rho'],
                                        'LogOddsRatio': row['LogOddsRatio']}

    def write_graph(self, filename):
        """
        Writes the interactions into a network file.
        """
        cx = CytoscapeXGMML()
        for n in self.nodes:
            cx.add_node(n, self.nodes[n])

        for e in self.edges:
            cx.add_edge(e[0], e[1], self.edges[e])

        print('Number of nodes:', len(cx.Graph.Nodes))
        print('Number of edges:', len(cx.Graph.Edges))
        cx.write_graph(filename)
