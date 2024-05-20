"""
Co-occurrence evaulation module 

This module calculates the co-occurrence from the count vectors of two microbial profiles from two samples.

"""

import numpy as np
from scipy.stats import fisher_exact


def coocurrence(v1, v2):
    """
    Co-occurrence Evaluation Using Fisher's Exact Test

    1. Convert the input vectors v1 and v2 into presence/absence vectors.
    2. Perform Fisher's exact test on the contingency table, which includes the number of co-occurring cases, cases occurring only in one vector, and cases where both are absent.
    3. Additionally, calculate the odds ratio of finding the number of co-occurring cases versus the expected value assuming independence.

    Returns:
        odds_ratio (float): The observed frequency divided by the expected frequency of independent cases.
        p_value (float): The p-value from Fisher's exact test.

    Reference:
    Chaffron, S., Rehrauer, H., Pernthaler, J., & Von Mering, C. (2010). A global network of coexisting microbes from environmental and whole-genome sequence data. Genome Research, 20(7), 947–959. https://doi.org/10.1101/gr.104521.109
    """

    # Extract non-zero indices
    nz1 = set(np.nonzero(v1)[0])
    nz2 = set(np.nonzero(v2)[0])

    # Count non-zero and co-occurrence
    n1 = len(nz1)
    n2 = len(nz2)

    n = len(v1)
    n12 = len(nz1.intersection(nz2))
    n1_2 = len(nz1 - nz2)
    n2_1 = len(nz2 - nz1)
    n_12 = n - n12 - n1_2 - n2_1

    # Create a contingency table
    ctable = [[n12, n1_2],
              [n2_1, n_12]]

    # Perform Fisher's exact test
    oddsratio, pv = fisher_exact(ctable)

    # Calculate probabilities
    n = len(v1)
    p1 = float(n1) / n
    p2 = float(n2) / n
    p12 = float(n12) / n

    # Calculate the likelihood ratio (odds ratio)
    if p1 == 0 or p2 == 0:
        odds_ratio = 1
    else:
        odds_ratio = p12 / (p1 * p2)

    return odds_ratio, pv
