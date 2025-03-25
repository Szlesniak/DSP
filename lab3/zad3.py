import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


from numpy.ma.core import concatenate
from scipy.signal.windows import chebwin

np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)

# N = 100
N = 1000
fs = 1000
A1 = 1
A2 = 0.0001
phi1 = np.pi/7
phi2 = np.pi/11
f1 = 100
f2 = 250

tmax = N/fs
t = np.linspace(0,tmax,N, endpoint=False)

x = A1 * np.cos(2 * np.pi * f1 * t + phi1) + A2 * np.cos(2 * np.pi * f2 * t + phi2)

fz = np.arange(0,500.1,0.1)
X3 = np.zeros(len(fz),dtype=complex)

for i,z in enumerate(x):
        X3 += (1/N) * z *np.exp( -1j * 2 * np.pi * i * fz/fs)

plt.plot(fz,np.imag(X3),'r-')
plt.show()
plt.plot(fz,np.real(X3))
plt.show()
n = np.arange(N)
#Prostokątne
window = np.zeros(N)
window[:int(N/2)] = 1

prost = x * window
Xp = np.zeros(len(fz),dtype=complex)

Xp = (1/N) * np.sum(prost * np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)


#Hamminga
ham = x*np.hamming(N)
Xh = np.zeros(len(fz),dtype=complex)

Xh = (1/N) * np.sum(ham * np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)


#Blackmana
Xb = np.zeros(len(fz),dtype=complex)
bla = x*np.blackman(N)

Xb = (1/N) * np.sum(bla *np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)

#Czebyszew  100dB
Xc1 = np.zeros(len(fz),dtype=complex)
cheby1 = chebwin(N,100)
cheby100 = x * cheby1
Xc1 = (1/N) * np.sum(cheby100 *np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)

#Czebyszew 120dB
Xc2 = np.zeros(len(fz),dtype=complex)
cheby2 = chebwin(N,120)
cheby120 = x*cheby2

Xc2 = (1/N) * np.sum(cheby120 * np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)

fig, axs = plt.subplots(5, 1, figsize=(0, 6), constrained_layout=True)
axs[0].plot(fz,20*np.log10(abs(Xh)), 'y-')
axs[0].set_title('Okno hamminga')
axs[0].set_xlabel('Częstotliwość [Hz}')
axs[0].set_ylabel('Amplituda')

axs[1].plot(fz,20*np.log10(abs(Xb)), 'r-')
axs[1].set_title('okno blackmana')
axs[1].set_xlabel('Częstotliwość [Hz}')
axs[1].set_ylabel('Amplituda')

axs[2].plot(fz,20*np.log10(abs(Xc1)), 'k-')
axs[2].set_title('okno czebyszewa 100dB')
axs[2].set_xlabel('Częstotliwość [Hz}')
axs[2].set_ylabel('Amplituda')

axs[3].plot(fz,20*np.log10(abs(Xc2)), 'r-')
axs[3].set_title('okno czebyszewa 120dB')
axs[3].set_xlabel('Częstotliwość [Hz}')
axs[3].set_ylabel('Amplituda')

axs[4].plot(fz,20*np.log10(abs(Xp)), 'b-')
axs[4].set_title('Okno Prostokątne')
axs[4].set_xlabel('Częstotliwość [Hz}')
axs[4].set_ylabel('Amplituda')
plt.show()