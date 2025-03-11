import numpy as np
from matplotlib import pyplot as plt

A = 230

f = 50
t = 0.1
fs1 = 10000



fs3 = 200

time1 = np.linspace(0, t, int(t*fs1))
time3 = np.linspace(0, t, int(t*fs3))

sig = A * np.sin(2*np.pi*f*time1)
plt.plot(time1, sig, 'b-')

sig2 = A * np.sin(2*np.pi*f*time3)
plt.plot(time3, sig2,'k-x')

T = 1/fs3
signal_reconstructed = np.zeros_like(time1)
for n in range(len(time1)):
    t_ = time1[n]
    signal_reconstructed[n] = np.sum(sig2*np.sinc((1/T)*(t_- time3)))
    print(t_-time3)
siggerr = sig - signal_reconstructed
plt.plot(time1, signal_reconstructed, 'r-')


plt.show()
plt.plot(time1, siggerr, 'b-')
plt.show()