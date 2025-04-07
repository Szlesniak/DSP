import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig

fs = 256000
As = 40
Ap = 1.1
fp = fs / 2 - 10000
fs1 = fs - fp

wp = 2 * np.pi * fp  # pasmo przepustowe
ws = 2 * np.pi * fs1  # pasmo zaporowe

N, wc = sig.buttord(wp, ws, Ap, As, analog=True)
z, p, k = sig.butter(N, wc, analog=True, output='zpk')
b, a = sig.butter(N, wc, analog=True, output='ba')

f = np.linspace(0, fs, fs, endpoint=False)
omega = 2 * np.pi * f

w, h = sig.freqs(b, a, worN=omega)

plt.figure(figsize=(6, 10))
circle = wc * np.exp(1j * np.linspace(3 * np.pi / 2, np.pi / 2, 1000))
plt.plot(np.real(circle), np.imag(circle), 'r--', label='Okrąg |s|=wc')
plt.plot(np.real(p), np.imag(p), 'o')
plt.show()

plt.plot(f, 20 * np.log10(abs(h)))
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.grid(True)
plt.title("Charakterystyka amplitudowa filtru Butterwortha")
plt.show()

N, rp = sig.cheb1ord(wp, ws, Ap, As, analog=True)
z, p, k = sig.cheby1(N, Ap, rp, output='zpk', analog=True)
b, a = sig.cheby1(N, Ap, rp, analog=True, output='ba')
w1, h1 = sig.freqs(b, a, worN=omega)

plt.figure(figsize=(6, 10))
plt.plot(np.real(p), np.imag(p), 'o')
plt.show()

plt.plot(f, 20 * np.log10(abs(h1)))
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.grid(True)
plt.title("Charakterystyka amplitudowa filtru Czebyszewa1")
plt.show()

# wp = 2 * np.pi * 170000
# ws = 2 * np.pi * (fs - 170000)

N, wn = sig.cheb2ord(wp, ws, Ap, As, analog=True)
z, p, k = sig.cheby2(N, As, wn, output='zpk', analog=True)
b, a = sig.cheby2(N, As, wn, analog=True, output='ba')
w2, h2 = sig.freqs(b, a, worN=omega)

plt.figure(figsize=(6, 10))
plt.plot(np.real(p), np.imag(p), 'o')
plt.show()

plt.plot(w2 / (2 * np.pi), 20 * np.log10(abs(h2)))
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.grid(True)
plt.title("Charakterystyka amplitudowa filtru Czebyszewa2")
plt.show()

N, wn = sig.ellipord(wp, ws, Ap, As, analog=True)
z, p, k = sig.ellip(N, Ap, As, wn, output='zpk', analog=True)
b, a = sig.ellip(N, Ap, As, wn, analog=True, output='ba')
w3, h3 = sig.freqs(b, a, worN=omega)

plt.plot(w2 / (2 * np.pi), 20 * np.log10(abs(h3)))
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.grid(True)
plt.title("Charakterystyka amplitudowa filtru Eliptycznego")
plt.show()
