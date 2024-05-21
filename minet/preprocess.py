"""
Preprocess the microbial feature tables to reduce less informative microbial features. 

- undersampling 
- filter by prevalence 
"""

import pandas as pd
import numpy as np


class Preprocessor:
    def __init__(self, table) -> None:
        self.table = table.copy()

    def undersampling_by_depth(self, depth_cutoff=10000):
        """
        Undersamples sequences reads for each samples
        """
        print(depth_cutoff)
        samples_to_drop = []
        for sample in self.table.columns:
            col = self.table[sample]
            total_reads = col.sum()
            if total_reads < depth_cutoff:
                samples_to_drop.append(sample)
                continue
            else:
                reads = col[col > 0].index.repeat(col[col > 0].values)
                undersampled_reads = np.random.choice(
                    reads, size=depth_cutoff, replace=False)
                undersampled_col = pd.Series(undersampled_reads).value_counts()
                undersampled_result = pd.Series(0, index=col.index)
                undersampled_result[undersampled_col.index] = undersampled_col.values
            self.table[sample] = undersampled_result

        for sp in samples_to_drop:
            self.table.drop(sp, axis=1, inplace=True)

    def filter_by_prevalence(self, prevalence_cutoff=0.1):
        """
        Filters ASVs by prevalence 
        """
        print(self.table.shape)
        m = self.table.shape[1]
        asvs_to_drop = []
        for id, row in self.table.iterrows():
            if float(np.count_nonzero(row)) / m <= prevalence_cutoff:
                asvs_to_drop.append(id)
        for asv in asvs_to_drop:
            self.table.drop(asv, axis=0, inplace=True)
