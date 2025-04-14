import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.signal as signal


mat = sio.loadmat('butter.mat')
z, p, k = mat['z'].flatten(), mat['p'].flatten(), mat['k'].item()

a = np.poly(p)
b = np.poly(z)
a = a / a[0]
b = b / b[0]
f = np.logspace(2,4,1000)
s = 1j * f * 2 * np.pi
X = np.polyval(b,s)
Y = np.polyval(a,s)

H = X / Y
X = X / max(abs(H))
H = X / Y
#^ część analogow
fs = 16000
T = 1/fs
def bilinear_transform(s_values,fs):
    z_values = []
    T = 1/fs
    for s in s_values:
        z = (1 + s*T/2) / (1 - s*T/2)  # Transformacja biliniowa: s = (2/T) * (z-1)/(z+1)
        z_values.append(z)
    return np.array(z_values)
#Część cyfrowa
z_digital = bilinear_transform(z,fs)
p_digital = bilinear_transform(p,fs)


b_digital = np.poly(z_digital)
a_digital = np.poly(p_digital)

a_digital = a_digital / a_digital[0]
b_digital = b_digital / a_digital[0]

f_digital, h_digital = signal.freqz(b_digital, a_digital, worN=4096, fs=fs)
h_digital = h_digital/max(np.abs(h_digital))

def pre_warp(f, fs):
    w = 2*np.pi*f
    T = 1/fs
    om = 2 * np.pi *f/fs
    return 2/ T * np.tan(om/2)
f1 = 1189
f2 = 1229
f1_pre = pre_warp(f1, fs)
f2_pre = pre_warp(f2, fs)
w1_pre = 2 * np.pi * f1_pre
w2_pre = 2 * np.pi * f2_pre
z1,p1,k1 = signal.buttap(len(p)//2)
a_lp = np.poly(p1)
b_lp = np.poly(z1) * k1

omega0 = np.sqrt(f1_pre*f2_pre)
bw = f2_pre - f1_pre
z_bp, p_bp, k_bp = signal.lp2bp_zpk(z1,p1,k1, omega0, bw)
a1 = np.poly(p_bp)
b1 = np.poly(z_bp) * k_bp
Hw = np.polyval(b1,s)/np.polyval(a1,s)

#warping
z1_digital = bilinear_transform(z_bp,fs) * k_bp
p1_digital = bilinear_transform(p_bp,fs)

a1_digital = np.poly(p1_digital)
b1_digital = np.poly(z1_digital)

f1_digital, h_digital_wrapped = signal.freqz(b1_digital, a1_digital, worN=4096, fs=fs)
h_digital_wrapped = h_digital_wrapped/max(np.abs(h_digital_wrapped))

plt.figure()
plt.semilogx(f, 20*np.log10(np.abs(H)), label='Analogowy')
plt.semilogx(f_digital, 20*np.log10(np.abs(h_digital)), label='Cyfrowy')
plt.axvline(1189, color='r', linestyle='--', label='Dolna granica (1189 Hz)')
plt.axvline(1229, color='g', linestyle='--', label='Górna granica (1229 Hz)')
plt.xlim(1000, 3000)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [dB]')
plt.legend()
plt.show()

plt.figure()
plt.semilogx(f, 20*np.log10(np.abs(H)), label='Analogowy')
plt.semilogx(f1_digital, 20*np.log10(np.abs(h_digital_wrapped)), label='Cyfrowy(warped)')
plt.axvline(1189, color='r', linestyle='--', label='Dolna granica (1189 Hz)')
plt.axvline(1229, color='g', linestyle='--', label='Górna granica (1229 Hz)')
plt.xlim(1000, 3000)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [dB]')
plt.legend()
plt.show()