import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.core import concatenate

np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)

N = 100
fs = 1000
A1 = 100
A2 = 200
phi1 = np.pi/7
phi2 = np.pi/11
f1 = 125
f2 = 200

tmax = N/fs
t = np.linspace(0,tmax,N, endpoint=False)

x = A1 * np.cos(2 * np.pi * f1 * t + phi1) + A2 * np.cos(2 * np.pi * f2 * t + phi2)

k = np.arange(N)
n = np.arange(N)
A = np.empty((N,N),dtype = np.complex128)

for i in n:
    for l in k:
        A[i,l] = 1/np.sqrt(N)*np.exp( -1j * 2 * np.pi * i * l / N )

X = A@x
f = np.arange(N)*fs/N

M = 100
xz = np.pad(x,(0,100),mode='constant',constant_values=0)
X2 = np.fft.fft(xz)/(N+M)
fx2 = np.arange(N+M)*fs/(N+M)
plt.plot(fx2,X2)
plt.show()
fz = np.linspace(0,fs,4000, endpoint=False)

X3 = np.zeros(len(fz),dtype=complex)
for i,x in enumerate(x):
        X3 += (1/N) * x *np.exp( -1j * 2 * np.pi * i * fz/fs)

plt.plot(fz,X3,'k-')
plt.show()
