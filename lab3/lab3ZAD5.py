import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import matplotlib
matplotlib.use('TkAgg')

np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)

mat = scipy.io.loadmat("rec_1m.mat")

y = mat['val'].flatten()
N = int(len(y))
x = y[:N]
fs = 500
tmax = 10
t = np.linspace(0,tmax,N,endpoint=False)
X = np.fft.fft(x)/len(x)
fz = np.linspace(0,tmax,20000,endpoint=False)
n = np.arange(N)
Xp = np.zeros(len(x),dtype=complex)
Xp = (1/N) * np.sum( x * np.exp( -1j * 2 * np.pi * n * fz[:,None]/fs),axis=1, dtype=np.complex128)


plt.plot(t,x[:N], label = "Sygnał")
plt.legend()
plt.show()
freq = np.fft.fftfreq(N, d=1/fs)
plt.plot(freq,abs(X),'r-', label="A(X)")
plt.legend()
plt.show()
plt.plot(freq,20*np.log10(abs(X)),'g-', label="amplituda X(dB)")
plt.legend()
plt.show()
plt.plot(fz,20*np.log10(abs(Xp)),'k-', label="amplituda Xp(dB)")
plt.legend()
plt.show()

plt.plot(fz, abs(Xp),'k-')
plt.show()

print(f'częstotliwość pracy serca = {freq[np.argmax(abs(X[0:len(freq/2)]))]} Hz')

