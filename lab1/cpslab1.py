import numpy as np
from matplotlib import pyplot as plt

A = 230
f = 50
t = 0.1
fs1 = 10000
fs2 = 500
fs3 = 200

time1 = np.linspace(0, t, int(t*fs1))
time2 = np.linspace(0, t, int(t*fs2))
time3 = np.linspace(0, t, int(t*fs3))
sig = A * np.sin(2*np.pi*f*time1)
plt.plot(time1, sig, 'b-')
sig1 = A * np.sin(2*np.pi*f*time2)
plt.plot(time2, sig1,'r-o')
sig2 = A * np.sin(2*np.pi*f*time3)
plt.plot(time3, sig2,'k-x')
plt.show()