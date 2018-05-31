import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
x = np.linspace(0.1,2,31)
y = np.linspace(-2,2,31)
X,Y = np.meshgrid(x,y)
Z = -np.log(X)+X*X+Y*Y/2-0.5
ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap='rainbow')
plt.show()