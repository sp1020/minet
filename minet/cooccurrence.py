import numpy as np
from scipy.stats import fisher_exact


def coocurrence(v1, v2):
    # === Co-occurrence evaluation using Fisher's exact test ===
    # 1. Convert the input vectors v1, v2 into the Presence/Absence vector
    # 2. Fisher's exact test for the contingency table with the number of co-occuring, occuring only in one vector, and both absence cases.
    # 3. Additionally calculate the odds ratio of finding the number of co-occuring cases vs. the expected value from the independent case
    #
    # Return
    # (1) odds ratio = observed frequency / expected frequency of independent cases
    # (2) P-value: Fisher's exact test
    #
    # Chaffron, S., Rehrauer, H., Pernthaler, J., & Von Mering, C. (2010). A global network of coexisting microbes from environmental and whole-genome sequence data. Genome Research, 20(7), 947–959. https://doi.org/\10.1101/gr.104521.109
    #

    nz1 = set(np.nonzero(v1)[0])
    nz2 = set(np.nonzero(v2)[0])

    n1 = len(nz1)
    n2 = len(nz2)

    n = len(v1)
    n12 = len(nz1.intersection(nz2))
    n1_2 = len(nz1 - nz2)
    n2_1 = len(nz2 - nz1)
    n_12 = n - n12 - n1_2 - n2_1

    ctable = [[n12, n1_2],
              [n2_1, n_12]]

    oddsratio, pv = fisher_exact(ctable)

    n = len(v1)
    p1 = float(n1) / n
    p2 = float(n2) / n
    p12 = float(n12) / n
    if p1 == 0 or p2 == 0:
        lr = 0
    else:
        lr = p12 / (p1 * p2)

    return lr, pv
