from scipy import io
import numpy as np
from matplotlib import pyplot as plt
mat = io.loadmat('adsl_x.mat')
print(mat)

x = mat['x'].flatten()

M = 32
K = 4
N = 512
indeks_prefiksu = np.zeros(K)
for i in range(K):
    prefix = x[(i+1)*(N-M)-1:(i+1)*N-1]
    corr = np.correlate(x,prefix,'full')
    indeks_prefiksu[i] = corr.argmax()
    print(int(indeks_prefiksu[i]- M + 1))

