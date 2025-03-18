import numpy as np
def myDCT(N):
    k = np.arange(N)
    n = np.arange(N)

    A = np.zeros((N, N))
    c = np.ones(N)
    skalar = np.zeros_like(n)
    c[0] = 1 / np.sqrt(2)
    for i in k:
        for j in n:
            A[j, i] = np.sqrt(2 / N) * c[i] * np.cos(((np.pi * i) / N) * (j + 0.5))
    return A