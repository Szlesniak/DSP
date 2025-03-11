import numpy as np
from matplotlib import pyplot as plt
fs = 100
t = 1
f0 = 0
df = 5
fe = 300
time = np.linspace(0, t, int(t*fs))
frequencies = np.linspace(f0,fe,int(fe/df+1))
print(len(frequencies))
print(frequencies)
sigs = []
for i,freq in enumerate(frequencies):
    sig = np.cos(2*np.pi*int(freq)*time)
    sigs.append(sig)
    plt.grid()
    plt.xlabel('t[s]')
    plt.plot(time, sig, label = str(i) +' '+ str(freq) + 'Hz')
    plt.legend()
    plt.show()

plt.subplot(3,1,1)
plt.title('Porównanie dla 5,105,205Hz')
plt.plot(time, sigs[1],'k-', label = '5Hz')
plt.plot(time,sigs[21],'r-',label = '105Hz')
plt.plot(time,sigs[41],'g-', label = '205Hz')
plt.legend()
plt.grid(True)

plt.subplot(3,1,2)
plt.title('Porównanie dla 95,195,295Hz')
plt.plot(time, sigs[19],'k-', label = '95Hz')
plt.plot(time,sigs[39],'r-',label = '195Hz')
plt.plot(time,sigs[59],'g-', label = '295Hz')
plt.grid(True)
plt.legend()

plt.subplot(3,1,3)
plt.title('Porównanie dla 95,105Hz')
plt.plot(time, sigs[19],time,sigs[21])
plt.plot(time, sigs[19],'k-', label = '95Hz')
plt.plot(time,sigs[21],'r-',label = '195Hz')
plt.legend(loc = 'upper right')
plt.grid(True)
plt.show()