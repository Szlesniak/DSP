import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import sounddevice as sd

def resample_signal(x, fs_in, fs_out):
    """Repróbkowanie sygnału z fs_in do fs_out przy użyciu up/downsampling + filtracji"""
    gcd = np.gcd(fs_in, fs_out)
    up = fs_out // gcd
    down = fs_in // gcd

    print(f"Upsampling by {up}, Downsampling by {down}")

    # Nadpróbkowanie
    x_upsampled = np.zeros(len(x) * up)
    x_upsampled[::up] = x

    # Filtr interpolujący (dolnoprzepustowy FIR)
    nyq_rate = 0.5 * fs_out
    cutoff = nyq_rate / max(up, down)  # Zabezpieczenie przed aliasingiem
    numtaps = 101
    fir_filter = signal.firwin(numtaps, cutoff / nyq_rate)

    # Filtracja
    x_filtered = signal.lfilter(fir_filter, 1.0, x_upsampled)

    # Decymacja
    x_resampled = x_filtered[::down]

    return x_resampled

# Wczytaj pliki
fs1, x1 = wav.read("x1.wav")
fs2, x2 = wav.read("x2.wav")

# Zamień na float w zakresie [-1, 1] jeśli dane są w int16
if x1.dtype != np.float32:
    x1 = x1.astype(np.float32) / np.max(np.abs(x1))
if x2.dtype != np.float32:
    x2 = x2.astype(np.float32) / np.max(np.abs(x2))

# Repróbkowanie do 48000 Hz
fs_target = 48000
if x1.ndim == 2:
    x1 = np.mean(x1, axis=1)
if x2.ndim == 2:
    x2 = np.mean(x2, axis=1)
x1_resampled = resample_signal(x1, fs1, fs_target)
x2_resampled = resample_signal(x2, fs2, fs_target)

# Ucięcie do wspólnej długości
min_len = min(len(x1_resampled), len(x2_resampled))
x1_resampled = x1_resampled[:min_len]
x2_resampled = x2_resampled[:min_len]

# Miksowanie (sumowanie z normalizacją)
x4 = x1_resampled + x2_resampled
x4 = x4 / np.max(np.abs(x4))  # Normalizacja

# Zapisz do pliku WAV
wav.write("x4.wav", fs_target, (x4 * 32767).astype(np.int16))

# Odtwarzanie do odsłuchu
print("Odtwarzanie zmiksowanego sygnału...")
sd.play(x4, fs_target)
sd.wait()