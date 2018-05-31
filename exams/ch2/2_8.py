import numpy
import sklearn.datasets as d
import matplotlib.pyplot as plt
reg_data = d.make_regression(100, 1, 1, 1, 1.0)
plt.plot(reg_data[0], reg_data[1])
plt.show()


x,y = d.make_classification(100, 2, 2, 0, 0, 2)
pos_x = x[y==1]
plt.scatter(pos_x[:,0], pos_x[:,1])
neg_x = x[y==0]
plt.scatter(neg_x[:,0], neg_x[:,1])
plt.show()
# print cls_data