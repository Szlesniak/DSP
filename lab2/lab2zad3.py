import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=8, suppress=True, linewidth=200, threshold = 100)
N = 100
fs = 1000
t = np.linspace(0, N/fs, N, endpoint = False)



# A1, f1 = 50, 50
# A2, f2 = 100, 100
# A3, f3 = 150, 150

# A1, f1 = 50, 50
# A2, f2 = 100, 107
# A3, f3 = 150, 150

A1, f1 = 50, 52.5
A2, f2 = 100, 102.5
A3, f3 = 150, 152.5



x = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t) + A3 * np.sin(2 * np.pi * f3 * t)

N = 100
k = np.arange(N)
n = np.arange(N)

A = np.zeros((N,N))
c = np.ones(N)
c[0] = 1/np.sqrt(2)

for i in k:
    for j in n:
        A[j,i] = np.sqrt(2/N)*c[i]*np.cos(((np.pi*i)/N)*(j+0.5))

S = np.transpose(A)
r = np.linspace(0, N ,N, endpoint = False)

# for l in range(N-1):
#     plt.plot(r, A[l,:],'ko')
#     plt.plot(r, S[:,l],'rx')
#     plt.show()

y = A@x
print(y)
plt.plot(y)
plt.title('oś x: 0:N')
plt.show()

f = np.arange(N)*fs/N/2

plt.figure(figsize=(10, 4))
plt.plot(t, x, label="Sygnał x(t)")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.title("Sygnał jako suma trzech sinusoid")
plt.legend()
plt.grid()
plt.show()

plt.plot(f,y)
plt.title('oś x: znormalizowana f')
plt.show()

xr = S@y
print(xr-x)