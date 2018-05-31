import numpy as np
def gd(x_start, step, g):   
    x = x_start
    for i in range(20):
        grad = g(x)
        x -= grad * step
        print ('[ Epoch {0} ] grad = {1}, x = {2}'.format(i, grad, x))
        if abs(grad) < 1e-6:
            break;
    return x

def f(x):
    return x * x  - 2 * x + 1

def g(x):
    return 3 * x - 2

import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-5,7,100)
y = f(x)
plt.plot(x, y)

gd(5,0.1,g)

gd(5,100,g)

gd(5,1,g)

gd(4,1,g)

def f2(x):
    return 4 * x * x - 4 * x + 1
def g2(x):
    return 8 * x - 4

gd(5,0.25,g2)

