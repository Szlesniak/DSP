import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
fs,flute = wav.read('flute.wav')
fs1,korg = wav.read('korg.wav')
np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)


flute = flute[:len(flute)//2]
korg = korg[:len(korg)//2]

freq1 = np.fft.fftfreq(len(flute), d=1/fs)
freq2 = np.fft.fftfreq(len(korg), d=1/fs)


Xf = np.fft.fft(flute)/len(flute)

Xk = np.fft.fft(korg)/len(korg)

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(freq2, np.abs(Xk))
plt.title('Widmo DFT - Korg')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')

plt.subplot(2, 1, 2)
plt.plot(freq1, np.abs(Xf))
plt.title('Widmo DFT - Flet')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.tight_layout()
plt.show()

flute = np.pad(flute, (0, korg.size - flute.size), mode='constant')
sum = flute + korg
N = len(flute)
Xsum = np.fft.fft(sum)/N
freq_sum = np.fft.fftfreq(N, d=1/fs)
plt.figure(figsize=(6, 3))
plt.plot(freq_sum, np.abs(Xsum))
plt.title('Widmo DFT - suma sygnałów')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.show()

cutoff_freq = 700
mask = np.abs(freq_sum) < cutoff_freq
Xsum[mask] *= 0.001

filtered_signal = np.fft.ifft(Xsum)
filtered_signal = filtered_signal.real
filtered_signal = filtered_signal
filtered_signal = (filtered_signal * 32767).astype(np.int16)
plt.plot(freq_sum, np.abs(Xsum))
plt.title('Widmo DFT - usunięcie (-700;700)Hz')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.show()
wav.write('sum.wav', fs, filtered_signal)