import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

fs = 10000
t = 1
fn = 50
fm = 1
m = 5
time = np.linspace(0, t, fs*t)

fs2 = 25
time2 = np.linspace(0, t, fs2*t)

sig = np.sin(2*np.pi*fn*time - (m/(2*np.pi*fm))*np.cos(2*np.pi*fm*time))
sigmodul = np.sin(2*np.pi*fm*time)
sig2 = np.sin(2*np.pi*fn*time2 - (m/(2*np.pi*fm))*np.cos(2*np.pi*fm*time2))
errorsfm = np.interp(time,time2,sig2)
err = sig - errorsfm


f,w1 = periodogram(sig,fs)

f1,w2 = periodogram(sig2,fs2)
plt.plot(time, sig,'k-')
plt.plot(time, sigmodul,'b-')
plt.show()
plt.plot(time, sig,'b-')
plt.plot(time2, sig2,'r-')
plt.show()
plt.plot(time,err,'r--')

plt.show()
plt.plot(f,w1,'b--')
plt.xlim(0,100)
plt.show()
plt.plot(f1,w2,'b--')
plt.xlim(0,10)
plt.show()
