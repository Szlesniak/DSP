import numpy as np


def dit(x):
    N = len(x)
    x = np.asarray(x)  # macierz wertykalna

    X1 = np.fft.fft(x[::2])  # próbki parzyste
    X2 = np.fft.fft(x[1::2])  # próbki nieparzyste

    X = np.zeros(N, dtype=complex)
    k = np.arange(N // 2)

    X[:N // 2] = X1 + np.exp(1j * 2 * np.pi / N * -k) * X2
    X[N // 2:] = X1 + np.exp(1j * 2 * np.pi / N * -(k + N // 2)) * X2

    return X