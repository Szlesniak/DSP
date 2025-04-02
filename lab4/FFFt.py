import numpy as np
from dit import dit
def FFFt(x):
    if (len(x) == 1 ):
        return x
    else:
        N = len(x)
        x = np.asarray(x)

        X1 = FFFt(x[::2])
        X2 = FFFt(x[1::2])

        X = np.zeros(N, dtype=complex)
        k = np.arange(N//2)
        W_N = np.exp(-2j * np.pi * k/N)

        X[:N//2] = X1 + W_N * X2
        X[N // 2:] = X1 - W_N * X2

        return X

