from math import log
import matplotlib.pyplot as plt
import numpy as np

def kl(p,q):
    return p * log(p / q) + (1 - p) * log((1 - p) / (1 - q))

def fisher(p):
    return 1 / p / (1 - p)

def fisher_kl(p,q):
    return 0.5 * fisher(p) * (p - q)*(p - q)

x = np.linspace(0.1, 0.9, 20)
y1 = [kl(0.5, q) for q in x]
y2 = [fisher_kl(0.5, q) for q in x]

plt.plot(x, y1, label='kl')
plt.plot(x, y2, label='fisher_kl')
plt.legend()
plt.show()