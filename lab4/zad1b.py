import numpy as np
from dit import dit
from FFFt import FFFt
N = 256
x = np.random.randn(N)
X1 = np.fft.fft(x)
X2 = dit(x)

error = np.mean(np.abs(X1 - X2))
print("Średni błąd:", error)

X3 = FFFt(x)

error = np.mean(np.abs(X1 - X3))
print("Średni błąd:", error)


