import numpy as np
import matplotlib.pyplot as plt


p = np.array([-0.5 - 9.5 * 1j, -0.5 + 9.5 * 1j, -1 - 10 * 1j, -1 + 10 * 1j, -0.5 - 10.5 * 1j,- 0.5 + 10.5 * 1j], dtype=np.complex64)
a = np.poly(p)

z = np.array([5 * 1j, -5 * 1j, 15 * 1j, -15 * 1j], dtype = np.complex64)

b = np.poly(z)
omega = np.linspace(0,20,1000)
s = 1j * omega
X = np.polyval(b, s )
Y = np.polyval(a, s )

H = X/Y
H = H/np.max(np.abs(H))

plt.plot(np.real(z), np.imag(z), 'bo', label = 'zera')
plt.plot(np.real(p), np.imag(p), 'r*', label = 'bieguny')
plt.xlabel('real')
plt.ylabel('imag')
plt.legend()
plt.show()

plt.plot(omega, abs(H))
plt.xlabel('jω')
plt.ylabel('|H(jω)|')
plt.title('Moduł transmitancji H(jω)')
plt.show()

plt.plot(omega, 20*np.log10(abs(H)))
plt.xlabel('jω')
plt.ylabel('20log10(|H(jω)|)')
plt.title('Skala logarytmiczna modułu transmitancji')
plt.show()

phi = np.angle(H, deg=True)

plt.plot(omega, phi)
plt.xlabel('jω')
plt.ylabel('phi')
plt.title('Cha-ka-fa-cz')
plt.show()


