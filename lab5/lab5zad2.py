import numpy as np
import matplotlib.pyplot as plt

w = np.pi * 2 * 100
N = 8
k = np.arange(N)

angles = np.pi * (0.5 + 0.5 / N + (k - 1) / N)
p = w * np.exp(1j * angles)

p = p[np.real(p) < 0]
den = np.poly(p)

f = np.linspace(0, 300, 1000)
omega = 2 * np.pi * f
s = 1j * omega
K = np.polyval(den, 0)

b = np.polyval([K], s)
a = np.polyval(den, s)

H = K / a
plt.plot(f, 20 * np.log10(abs(H)))
plt.show()
