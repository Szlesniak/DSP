import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import sounddevice as sd
from scipy.interpolate import interp1d
from scipy.signal import get_window


def resample_signal(x, fs_in, fs_out):
    """Repróbkowanie sygnału z fs_in do fs_out przy użyciu up/downsampling + filtracji"""
    gcd = np.gcd(fs_in, fs_out)
    up = fs_out // gcd
    down = fs_in // gcd

    print(f"Upsampling by {up}/ Downsampling by {down}")

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

def resample_linear(x, fs_in, fs_out, duration):
    """Interpolacja liniowa"""
    t_in = np.arange(0, duration, 1/fs_in)
    t_out = np.arange(0, duration, 1/fs_out)
    interp_func = interp1d(t_in, x, kind='linear', fill_value="extrapolate")
    return interp_func(t_out)

def resample_sinc(x, fs_in, fs_out, duration, L=100):
    """Rekonstrukcja sygnału metodą splotu z sinc"""
    t_out = np.arange(0, duration, 1/fs_out)
    t_in = np.arange(0, duration, 1/fs_in)

    # Macierz czasu różnicy
    T = t_out[:, None] - t_in[None, :]
    h = np.sinc(T * fs_in)  # funkcja sinc

    return h @ x  # splot macierzowy (każdy punkt t_out jako suma ważona próbek wejściowych)


def sinc_interp(x, fs_in, fs_out, window='blackman', num_taps=64):
    """
    Zmiana częstotliwości próbkowania sygnału x z fs_in do fs_out
    przy użyciu interpolacji sinc z oknem.

    Parametry:
    - x: sygnał wejściowy (1D numpy array)
    - fs_in: oryginalna częstotliwość próbkowania
    - fs_out: docelowa częstotliwość próbkowania
    - window: typ okna (np. 'blackman')
    - num_taps: liczba współczynników filtru

    Zwraca:
    - x_resampled: sygnał po zmianie częstotliwości próbkowania
    """
    # Obliczenie współczynnika zmiany częstotliwości
    ratio = fs_out / fs_in
    n = np.arange(-num_taps // 2, num_taps // 2 + 1)
    sinc_func = np.sinc(n / ratio)

    # Zastosowanie okna
    window_vals = get_window(window, num_taps + 1)
    kernel = sinc_func * window_vals
    kernel /= np.sum(kernel)

    # Obliczenie liczby próbek w sygnale wyjściowym
    num_output_samples = int(len(x) * ratio)

    # Interpolacja
    x_resampled = np.zeros(num_output_samples)
    for i in range(num_output_samples):
        t = i / ratio
        left = int(np.floor(t)) - num_taps // 2
        right = left + num_taps + 1
        x_segment = x[max(left, 0):min(right, len(x))]
        k_left = max(0, -left)
        k_right = k_left + len(x_segment)
        x_resampled[i] = np.dot(x_segment, kernel[k_left:k_right])
    return x_resampled


def sinc_interp(x, fs_in, fs_out, window='blackman', num_taps=64):
    """
    Zmiana częstotliwości próbkowania sygnału x z fs_in do fs_out
    przy użyciu interpolacji sinc z oknem.

    Parametry:
    - x: sygnał wejściowy (1D numpy array)
    - fs_in: oryginalna częstotliwość próbkowania
    - fs_out: docelowa częstotliwość próbkowania
    - window: typ okna (np. 'blackman')
    - num_taps: liczba współczynników filtru

    Zwraca:
    - x_resampled: sygnał po zmianie częstotliwości próbkowania
    """
    # Obliczenie współczynnika zmiany częstotliwości
    ratio = fs_out / fs_in
    n = np.arange(-num_taps // 2, num_taps // 2 + 1)
    sinc_func = np.sinc(n / ratio)

    # Zastosowanie okna
    window_vals = get_window(window, num_taps + 1)
    kernel = sinc_func * window_vals
    kernel /= np.sum(kernel)

    # Obliczenie liczby próbek w sygnale wyjściowym
    num_output_samples = int(len(x) * ratio)

    # Interpolacja
    x_resampled = np.zeros(num_output_samples)
    for i in range(num_output_samples):
        t = i / ratio
        left = int(np.floor(t)) - num_taps // 2
        right = left + num_taps + 1
        x_segment = x[max(left, 0):min(right, len(x))]
        k_left = max(0, -left)
        k_right = k_left + len(x_segment)
        x_resampled[i] = np.dot(x_segment, kernel[k_left:k_right])
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
x4_mix = x1_resampled + x2_resampled
x4_mix = x4_mix / np.max(np.abs(x4_mix))  # Normalizacja
x4_mix = x4_mix * 0.01

# Zapisz do pliku WAV
wav.write("x4.wav", fs_target, (x4_mix * 32767//32).astype(np.int16))

# Odtwarzanie do odsłuchu
print("Odtwarzanie zmiksowanego sygnału...")
sd.play(x4_mix, fs_target)
sd.wait()


# Parametry sinusoid
f1, fs1 = 1001.2, 8000
f2, fs2 = 303.1, 32000
f3, fs3 = 2110.4, 48000
duration = 1.0
fs_target = fs3  # 48000 Hz

# Czas dla każdej z częstotliwości próbkowania
t1 = np.arange(0, duration, 1/fs1)
t2 = np.arange(0, duration, 1/fs2)
t3 = np.arange(0, duration, 1/fs3)

# Sygnały sinusoidalne
x1 = np.sin(2 * np.pi * f1 * t1)
x2 = np.sin(2 * np.pi * f2 * t2)
x3 = np.sin(2 * np.pi * f3 * t3)

# Repróbkowanie x1 i x2 do fs3
x1_resampled = resample_signal(x1, fs1, fs_target)
x2_resampled = resample_signal(x2, fs2, fs_target)
# x3 już jest w fs3 – nie trzeba resamplować

x1_lin = resample_signal(x1, fs1, fs_target)
x2_lin = resample_signal(x2, fs2, fs_target)

x1_sinc = resample_signal(x1, fs1, fs_target)
x2_sinc = resample_signal(x2, fs2, fs_target)

x1_soxr = sinc_interp(x1,fs1,fs_target)
x2_soxr = sinc_interp(x2,fs2,fs_target)


# Ucięcie do wspólnej długości (wszystkie powinny mieć tę samą długość 48000)
min_len = min(len(x1_resampled), len(x2_resampled), len(x3))
x1_resampled = x1_resampled[:min_len]
x2_resampled = x2_resampled[:min_len]
x3 = x3[:min_len]

x1_lin = x1_lin[:min_len]
x2_lin = x2_lin[:min_len]

x1_sinc = x1_sinc[:min_len]
x2_sinc = x2_sinc[:min_len]

x1_soxr = x1_soxr[:min_len]
x2_soxr = x2_soxr[:min_len]

# Sumowanie i normalizacja
x4 = x1_resampled + x2_resampled + x3
x4 = x4 / np.max(np.abs(x4))  # Normalizacja
x4 = 0.01 * x4

x4_lin = x1_lin + x2_lin + x3
x4_lin = x4_lin/np.max(np.abs(x4_lin))
x4_lin = 0.01 * x4_lin

x4_sinc = x1_sinc + x2_sinc + x3
x4_sinc = x4_sinc/np.max(np.abs(x4_sinc))
x4_sinc = x4_sinc * 0.01

x4_soxr = x1_soxr + x2_soxr + x3
x4_soxr = x4_soxr/np.max(np.abs(x4_soxr))
x4_soxr = x4_soxr * 0.01

# Zapis do WAV i odtwarzanie
wav.write("x4_synt.wav", fs_target, (x4 * 32767//32).astype(np.int16))
print("Odtwarzanie zmiksowanego sygnału syntetycznego...")
sd.play(x4, fs_target)
sd.wait()

wav.write("x4_lin.wav", fs_target, (x4_lin * 32767//32).astype(np.int16))
print("Odtwarzanie zmiksowanego sygnału syntetycznego(lin)...")
sd.play(x4_lin, fs_target)
sd.wait()

wav.write("x4_sinc.wav", fs_target, (x4_sinc * 32767//32).astype(np.int16))
print("Odtwarzanie zmiksowanego sygnału syntetycznego(sinc)...")
sd.play(x4_sinc, fs_target)
sd.wait()

wav.write("x4_sinc_interp.wav", fs_target, (x4_soxr * 32767//32).astype(np.int16))
print("Odtwarzanie zmiksowanego sygnału syntetycznego(soxr)...")
sd.play(x4_sinc, fs_target)
sd.wait()
