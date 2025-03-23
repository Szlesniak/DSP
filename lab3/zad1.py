import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)

N = 100
fs = 1000
A1 = 100
A2 = 200
phi1 = np.pi/7
phi2 = np.pi/11
f1 = 100
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
plt.plot(f, np.imag(X), 'r-')
plt.title('Imag(X)')
plt.show()
plt.plot(f, np.real(X), 'b-')
plt.title('Real(X)')
plt.show()
plt.plot(f, abs(X), 'g-')
plt.title('abs(X)')
plt.show()
plt.plot(f, np.angle(X), 'r-')
plt.title('Phase(X)')
plt.show()

B = np.conj(A.transpose())

xr = B@X
print(xr-x)

X1 = np.fft.fft(x)
xr1 = np.fft.ifft(X1)

print(x-xr1)




