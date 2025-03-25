import numpy as np
import scipy.io
from matplotlib import pyplot as plt
# Wczytanie pliku .mat
mat = scipy.io.loadmat("lab_03.mat") # wczytanie plików danych z matlab
x = mat[f'x_{420035%6 + 1}'].flatten()  # pobranie danych zmiennej x z pliku .mat, i konwersja na jednowymierową macierz
M = 32
N = 512
K = 8
fs = 2200000

for i in range(K):
    start = i * (M + N) + M
    ramka = x[start:start + N]

    X = np.fft.fft(ramka)
    freq = np.linspace(0, fs, N, endpoint=False) - fs/2 # Skala częstotliwości
    # freq = np.fft.fftfreq(N, 1/fs)
    X = np.fft.fftshift(X)


    plt.plot(freq[:N//2], np.abs(X[:N//2]))
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda")
    plt.title(f"FFT Ramki {i+1}")
    plt.grid()
    plt.show()


    threshold = 0.9 * np.max(np.abs(X))
    harmonic = freq[np.abs(X) > threshold]

    print(f"Ramka {i+1}: Wykryte harmoniczne:", harmonic)
