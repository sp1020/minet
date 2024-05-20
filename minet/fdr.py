"""
This module facilitate evaluation of statistical significance for multiple test cases by controling the false discovery rate.

The FDR class handles a DataFrame object and calculates adjusted p-values for individual tests.
"""

import pandas as pd
from statsmodels.stats import multitest


class FDR:
    """
    Handles multiple test results to calculate adjusted p-values, thereby controlling the false discovery rate (FDR). 
    """

    def __init__(self):
        """
        Initializes the FDR analysis class 
        """
        self.pvalue_names = ['P.value', 'P-value', 'p-value', 'p.value']

    def calc(self, data, pvalue_index=None, alpha=0.05):
        """
        Adjusts p-values in the DataFrame for multiple testing using FDR control.

        Parameters:
        data (pd.DataFrame): Input data containing p-values.
        alpha (float): Significance level for the FDR adjustment.
        pvalue_index (str, optional): Column name for p-values. If None, searches for p-value columns in self.pvalue_names.

        Returns:
        pd.DataFrame: DataFrame with adjusted p-values and significance flags.
        pd.DataFrame: DataFrame containing only the adjusted p-values and significance flags.
        """

        # Check the input data type
        if not isinstance(data, pd.DataFrame):
            raise TypeError('Input data should be pandas.DataFrame type.')

        # Extract p-values
        if pvalue_index:
            ps = data[pvalue_index]
        else:
            flag_found = False
            for pn in self.pvalue_names:
                if pn in data.columns:
                    ps = data[pn]
                    flag_found = True
                    break
            if not flag_found:
                raise KeyError('There is no column matching P-values: %s'
                               % ', '.join(self.pvalue_names))

        # Sort by P-values
        ps = ps.sort_values()

        # Adjust p-values using FDR
        res = multitest.multipletests(ps.values, alpha=alpha, method='fdr_bh')
        (rej, p_cor, alpha_sidak, alpha_bonf) = res

        # Prepare result DataFrame
        ix_name = ps.index.name
        dt = {ix_name: ps.index,
              'Adjusted-P': p_cor,
              'Significance': rej}

        df = pd.DataFrame.from_dict(dt)
        df = df.set_index(ix_name)

        # Concatenate the original DataFrame with the results
        res = pd.concat([data, df], axis=1)
        return res, df
