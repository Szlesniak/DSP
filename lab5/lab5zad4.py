import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# === 7_4.m === Analogowy filtr prototypowy i transformacja częstotliwości

# Parametry
N = 8
f0 = 100  # dla LP oraz HP
f1 = 10
f2 = 100  # dla BP oraz BS
Rp = 3
Rs = 100

# Wybór filtra prototypowego (tylko jeden aktywny na raz)
z, p, k = signal.buttap(N)           # Butterworth
# z, p, k = signal.cheb1ap(N, Rp)    # Chebyshev typu I
# z, p, k = signal.cheb2ap(N, Rs)    # Chebyshev typu II
# z, p, k = signal.ellipap(N, Rp, Rs) # Eliptyczny (Cauer)

# Przekształcenie prototypu do postaci transmitancji H(s)
b = k * np.poly(z)
b = [b]
a = np.poly(p)

# Zakres częstotliwości
f = np.arange(0, 1000.01, 0.01)
w = 2 * np.pi * f

# Charakterystyka amplitudowa prototypu
w_proto, H_proto = signal.freqs(b, a, w)
plt.figure()
plt.semilogx(w_proto, 20 * np.log10(np.abs(H_proto)))
plt.grid()
plt.xlabel('w [rad/s]')
plt.title('Analog Proto |H(f)|')
plt.show()

# Zera i bieguny prototypu
fi = np.linspace(0, 2*np.pi, 1000)
c = np.cos(fi)
s = np.sin(fi)
plt.figure()
plt.plot(np.real(z), np.imag(z), 'ro', label='Zera')
plt.plot(np.real(p), np.imag(p), 'b*', label='Bieguny')
plt.plot(c, s, 'k--', label='Jednostkowe koło')
plt.title('Analog Proto Zera i Bieguny')
plt.xlabel('Re'); plt.ylabel('Im')
plt.grid()
plt.legend()
plt.axis('equal')
plt.show()

# === Transformacja częstotliwości ===
# Odkomentuj jedną linię w zależności od typu filtra docelowego

b, a = signal.lp2lp(b, a, 2*np.pi*f0)        # LP → LP
# b, a = signal.lp2hp(b, a, 2*np.pi*f0)      # LP → HP
# b, a = signal.lp2bp(b, a, 2*np.pi*np.sqrt(f1*f2), 2*np.pi*(f2-f1))  # LP → BP
# b, a = signal.lp2bs(b, a, 2*np.pi*np.sqrt(f1*f2), 2*np.pi*(f2-f1))  # LP → BS

f = np.arange(0, 1000.1, 0.1)  # Częstotliwość w Hz
w = 2 * np.pi * f
s = 1j * w
H = np.polyval(b, s) / np.polyval(a, s)

plt.figure()
plt.plot(f, 20 * np.log10(np.abs(H)))
plt.xlabel('f [Hz]')
plt.ylabel('|H(f)| [dB]')
plt.title('Charakterystyka amplitudowa')
plt.grid()
plt.show()

plt.figure()
plt.plot(f, np.unwrap(np.angle(H)))
plt.xlabel('f [Hz]')
plt.ylabel('Faza [rad]')
plt.title('Charakterystyka fazowa')
plt.grid()
plt.show()

# Odpowiedź impulsowa
system = signal.TransferFunction(b, a)
t_imp, y_imp = signal.impulse(system)
plt.figure()
plt.plot(t_imp, y_imp)
plt.xlabel('Czas [s]')
plt.ylabel('Odpowiedź impulsowa')
plt.title('Odpowiedź impulsowa filtra')
plt.grid()
plt.show()

# Odpowiedź skokowa
t_step, y_step = signal.step(system)
plt.figure()
plt.plot(t_step, y_step)
plt.xlabel('Czas [s]')
plt.ylabel('Odpowiedź skokowa')
plt.title('Odpowiedź skokowa filtra')
plt.grid()
plt.show()