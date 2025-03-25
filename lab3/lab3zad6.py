import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
fs,flute = wav.read('flute.wav')
fs1,korg = wav.read('korg.wav')
np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)


flute = flute[:len(flute)//2]
korg = korg[:len(korg)//2]
flute = np.pad(flute, (0, korg.size - flute.size), mode='constant')

N = len(flute)
tmax = N//fs
t = np.linspace(0, tmax, N)

Xf = np.fft.fft(flute)
Xk = np.fft.fft(korg)
freq = np.fft.fftfreq(N, d=1/fs)
