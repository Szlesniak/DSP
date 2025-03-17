import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 8)

N = 20
k = np.arange(N)
n = np.arange(N)

w = np.zeros((N,N))
c = np.ones(N)
skalar = np.zeros_like(n)
c[0] = 1/np.sqrt(2)
for i in k:
    for j in n:
        w[j,i] = np.sqrt(2/N)*c[i]*np.cos(((np.pi*i)/N)*(j+0.5))


for i in range(N-1):
    skalar[i] = np.dot(w[i,:],w[i+1,:])
#
# print(skalar)
# print(w)

S = np.transpose(w)
# print((S@w))

x = np.random.randn(N)
X = w@np.transpose(x)

xs = S@X

print(xs - x)