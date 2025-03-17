import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True, linewidth=200, threshold = 32)

def cross_correlation(x, y):
    lenX = len(x)
    lenY = len(y)
    correlation = np.zeros(lenX + lenY - 1)

    y = y[::1]

    # Obliczanie korelacji
    for k in range(lenX + lenY - 1):
        sum_val = 0
        for l in range(lenX):
            if 0 <= k - l < lenY:
                sum_val += x[l] * y[k - l]
        correlation[k] = sum_val

    return correlation[::1]


adsl = sio.loadmat('adsl_x.mat')
x = adsl['x'].flatten()

M = 32
N = 512
K = 4

bestPrefix = list()
bestScore = list()
prefixPoz = list()
y = 0

# Dla gotowej funkcji
for i in range(len(x)):
    # iterowanie od 0
    prefix = x[i:i + M]
    correlation = np.correlate(x, prefix, 'full')
    y = max(correlation)
    z = np.where(correlation == y)[0]
    if len(z) >= 2:
        bestPrefix.append(prefix)
        bestScore.append(correlation)
        prefixPoz.append(i)

for i in range(len(bestScore)):
    plt.axvline(prefixPoz[i], color='red')
    if i % 2 == 1:
        plt.plot(bestScore[i])
        plt.show()

print(bestPrefix)
print(y)
print(prefixPoz)

# for i in range(len(x)):
#     print(i)
#     # iterowanie od 0
#     prefix = x[i:i + M]
#     correlation = cross_correlation(x, prefix)
#     y = max(correlation)
#     z = np.where(correlation == y)[0]
#     if len(z) >= 2:
#         bestPrefix.append(prefix)
#         bestScore.append(correlation)
#         prefixPoz.append(i-M)


# print(bestPrefix)
# print(y)
# print(prefixPoz)

