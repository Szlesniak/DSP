import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

f_p1 = 95e6  # dolna granica pasma przepustowego [Hz]
f_p2 = 97e6  # górna granica pasma przepustowego [Hz]
f_s1 = 94.5e6  # dolna granica pasma zaporowego [Hz]
f_s2 = 97.5e6  # górna granica pasma zaporowego [Hz]

wp = [2 * np.pi * f_p1, 2 * np.pi * f_p2]
ws = [2 * np.pi * f_s1, 2 * np.pi * f_s2]
rp = 1

gpass = 3  # maksymalne zafalowanie w paśmie przepustowym [dB]
gstop = 40  # minimalne tłumienie w paśmie zaporowym [dB]

N, Wn = signal.cheb2ord(wp, ws, gpass, gstop, analog=True)

print("TESTOWY FILTR:")
print(f"Rząd filtru: {N}")
print(f"Częstotliwości graniczne (rad/s): {Wn}")
print(f"Częstotliwości graniczne (Hz): {[w / (2 * np.pi) for w in Wn]}")

b, a = signal.cheby2(N, 40, Wn, btype='bandpass', analog=True)
f = np.linspace(93e6, 99e6, 10000, endpoint=False)
omega = 2 * np.pi * f
w, H = signal.freqs(b, a, omega)
plt.plot(f, 20 * np.log10(abs(H)), label="|H(f)|[dB]")
plt.axvline(f_p1, color='green', linestyle='--', label="Pasmo przepustowe")
plt.axvline(f_p2, color='green', linestyle='--')
plt.grid()
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie [dB]")
plt.title("Charakterystyka testowego filtru (±1 MHz)")
plt.legend()
plt.show()

f_p1 = 95.9e6  # dolna granica pasma przepustowego [Hz]
f_p2 = 96.1e6  # górna granica pasma przepustowego [Hz]
f_s1 = 95.5e6  # dolna granica pasma zaporowego [Hz]
f_s2 = 96.5e6  # górna granica pasma zaporowego [Hz]

wp = [2 * np.pi * f_p1, 2 * np.pi * f_p2]
ws = [2 * np.pi * f_s1, 2 * np.pi * f_s2]
rp = 1

gpass = 3  # maksymalne zafalowanie w paśmie przepustowym [dB]
gstop = 40  # minimalne tłumienie w paśmie zaporowym [dB]

N, Wn = signal.cheb2ord(wp, ws, gpass, gstop, analog=True)

print("TESTOWY FILTR:")
print(f"Rząd filtru: {N}")
print(f"Częstotliwości graniczne (rad/s): {Wn}")
print(f"Częstotliwości graniczne (Hz): {[w / (2 * np.pi) for w in Wn]}")

b, a = signal.cheby2(N, gstop, Wn, btype='bandpass', analog=True)
f = np.linspace(93e6, 99e6, 10000, endpoint=False)
omega = 2 * np.pi * f
w, H = signal.freqs(b, a, omega)
plt.plot(f, 20 * np.log10(abs(H)), label="|H(f)|[dB]")
plt.axvline(f_p1, color='green', linestyle='--', label="Pasmo przepustowe")
plt.axvline(f_p2, color='green', linestyle='--')
plt.grid()
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie [dB]")
plt.title("Charakterystyka filtru (±1 kHz)")
plt.legend()
plt.show()



p = np.array([2 - 6 * 1j, 2 + 6 * 1j, 2 - 10 * 1j, 2 + 10 * 1j, 2 - 14 * 1j, 2 + 14 * 1j],
             dtype=np.complex64)

z = np.array([5 * 1j, -5 * 1j, 15 * 1j, -15 * 1j], dtype=np.complex64)

a = np.poly(p)
b = np.poly(z)
dab = np.linspace(0, 20, 1000)
s = 1j * dab
X = np.polyval(b, s)
Y = np.polyval(a, s)

H = X / Y

plt.plot(dab/2/np.pi, 20 * np.log10(abs(H)), label="|H(f)|[dB]")
plt.grid()
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie [dB]")
plt.title("Charakterystyka filtru (±1 kHz)")
plt.legend()
plt.show()
