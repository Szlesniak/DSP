import numpy as np
from matplotlib import pyplot as plt
f = 50
t = 1
fs1 = 10000
fs2 = 51
fs3 = 50
fs4 = 49
time1 = np.linspace(0, t, int(t*fs1))
time2 = np.linspace(0, t, int(t*fs2))
time3 = np.linspace(0, t, int(t*fs3))
time4 = np.linspace(0, t, int(t*fs4))

sig1 = np.sin(np.pi*2*f*time1)
plt.plot(time1, sig1)
sig2 = np.sin(np.pi*2*f*time2)
plt.plot(time2, sig2,'g-o', label = '51Hz')
sig3 = np.sin(np.pi*2*f*time3)
plt.plot(time3, sig3,'r-o', label = '50Hz')
sig4 = np.sin(np.pi*2*f*time4)
plt.plot(time4, sig4,'k-o', label = '49Hz')
plt.legend()
plt.show()

fs5 = 26
fs6 = 25
fs7 = 24
time5 = np.linspace(0, t, int(t*fs5))
time6 = np.linspace(0, t, int(t*fs6))
time7 = np.linspace(0, t, int(t*fs7))
sig5 = np.sin(np.pi*2*f*time5)
plt.plot(time5, sig5)
sig6 = np.sin(np.pi*2*f*time6)
plt.plot(time6, sig6,'g-o')
sig7 = np.sin(np.pi*2*f*time7)
plt.plot(time7, sig7,'r-o')
plt.grid()
plt.show()