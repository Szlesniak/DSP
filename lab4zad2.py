import numpy as np
import matplotlib.pyplot as plt

# Parameters
fpr = 1000  # Sampling frequency (Hz)
N = 100  # Number of samples, 100 or 1000
dt = 1 / fpr  # Time step
t = dt * np.arange(N)  # Time vector

# Signal
f0 = 200  # Frequency of the signal
x = 10 * np.sin(2 * np.pi * f0 * t)  # Signal

# Plot time-domain signal
plt.figure()
plt.plot(t, x, 'bo-')
plt.xlabel('t [s]')
plt.title('x(t)')
plt.grid(True)
plt.pause(0.1)

# FFT spectrum
X = np.fft.fft(x)
X = 20*np.log10(2/N*abs(X))
f = fpr / N * np.arange(N/2)  # Frequency vector

# Plot FFT magnitude
plt.figure()
plt.plot(f, np.abs(X[:N//2]) * 2 / N, 'bo-')
plt.xlabel('f [Hz]')
plt.title('|X(k)|')
plt.grid(True)
plt.pause(0.1)

plt.show()
