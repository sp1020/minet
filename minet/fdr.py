import pandas as pd
import numpy as np
from statsmodels.stats import multitest


class FDR:
    def __init__(self):
        self.pvalue_names = ['P.value', 'P-value', 'p-value', 'p.value']

    def calc(self, data, pvalue_index=None, alpha=0.05):
        if not isinstance(data, pd.DataFrame):
            raise TypeError('Input data should be pandas.DataFrame type.')

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

        res = multitest.multipletests(ps.values, alpha=alpha, method='fdr_bh')
        (rej, p_cor, alpha_sidak, alpha_bonf) = res

        ix_name = ps.index.name
        dt = {ix_name: ps.index,
              'Adjusted-P': p_cor,
              'Significance': rej}

        df = pd.DataFrame.from_dict(dt)
        df = df.set_index(ix_name)

        # Concatenate dataframe
        res = pd.concat([data, df], axis=1)
        return res, df
