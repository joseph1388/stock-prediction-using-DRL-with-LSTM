import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = np.linspace(0.01,0.99,101)
Y = np.linspace(0.01,0.99,101)
X,Y = np.meshgrid(X,Y)
Z = -X * np.log2(Y) - (1-X)* np.log2(1 - Y)
ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap='rainbow')
plt.show()