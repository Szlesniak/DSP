from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from myDCT import myDCT

x = read('mowa.wav')
signal = x[1]
fs = x[0]
print(fs)
plt.plot(signal)
plt.show()

A = myDCT(256)
M =10
N = 256
samples = np.zeros((M,N))
l = [2000,4000,12000,13000,17500,18000,20000,25000,33000,35000]

for k in range(M):
    samples[k,:] = signal[l[k]:l[k]+N]

f = np.arange(N)*fs/N/2

for o in range(M):
    plt.subplot(2,1,1)
    y = samples[o,:]
    plt.plot(y, label = f'próbki {l[o]}:{l[o]+N}')
    plt.legend()
    plt.subplot(2,1,2)
    yk = A@y
    plt.plot(f,yk,label = 'DCT' )
    plt.legend()
    plt.show()
