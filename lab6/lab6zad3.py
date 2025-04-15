import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, welch
from scipy.io.wavfile import write

# --- Parametry ---
fs = 3.2e6          # Częstotliwość próbkowania
N = int(32e6)       # Liczba próbek IQ
fc = 0.5e6          # Przesunięcie częstotliwości nośnej
bwSERV = 80e3       # Pasmo jednej stacji
bwAUDIO = 16e3      # Pasmo audio

# --- Wczytanie danych ---
with open('samples_100MHz_fs3200kHz.raw', 'rb') as f:
    s = np.frombuffer(f.read(2 * N), dtype=np.uint8)

s = s.astype(np.float32) - 127.0
wideband_signal = s[0::2] + 1j * s[1::2]
del s

# --- Przesunięcie stacji do pasma podstawowego ---
n = np.arange(N)
wideband_signal_shifted = wideband_signal * np.exp(-1j * 2 * np.pi * fc / fs * n)

# --- Filtracja (Butterworth LPF 4. rzędu, fc = 80kHz) ---
def butter_lowpass(cutoff, fs, order=4):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    return butter(order, norm_cutoff, btype='low')

b, a = butter_lowpass(bwSERV, fs)
wideband_signal_filtered = lfilter(b, a, wideband_signal_shifted)

# --- Dekymacja do 80 kHz ---
x = wideband_signal_filtered[::int(fs / bwSERV)]

# --- Demodulacja FM ---
dx = x[1:] * np.conj(x[:-1])
y = np.arctan2(np.imag(dx), np.real(dx))

# --- Filtracja antyaliasingowa (fc = 16kHz przy fs = 3.2MHz) ---
b_aa, a_aa = butter_lowpass(bwAUDIO, fs)
y_filtered = lfilter(b_aa, a_aa, y)

# --- Dekymacja do 16 kHz ---
ym = y_filtered[::int(bwSERV / bwAUDIO)]

# --- Normalizacja i zapis do WAV ---
ym = ym - np.mean(ym)
ym = ym / (1.001 * np.max(np.abs(ym)))

write("output_fm.wav", int(bwAUDIO), ym.astype(np.float32))
print("Zapisano plik 'output_fm.wav'")

# --- Funkcja do rysowania ---
def plot_time_and_psd(signal, fs, title):
    plt.figure(figsize=(12, 4))
    t = np.arange(len(signal)) / fs

    plt.subplot(1, 2, 1)
    plt.plot(t, signal)
    plt.title(f'{title} - przebieg czasowy')
    plt.xlabel("Czas [s]")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    f, Pxx = welch(signal, fs=fs, window='hamming', nperseg=1024)
    plt.semilogy(f, Pxx)
    plt.title(f'{title} - widmo (Welch)')
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Gęstość mocy [dB/Hz]")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# --- Wykres końcowego sygnału audio ---
plot_time_and_psd(ym, bwAUDIO, "Sygnał audio (po filtracji i dekymacji)")
