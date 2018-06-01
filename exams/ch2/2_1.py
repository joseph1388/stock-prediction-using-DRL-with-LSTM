import numpy as np

A = np.array([
  [1, 0, 0],
  [0, 1, 0],
  [1, 1, 0]
])
b = np.array([1, 1,1])
print (np.dot(A.T, b))
# array([2, 2, 0])

A = np.array([
  [1, 0, 0],
  [0, 1, 0]
])
b = np.array([2, 2, 0])
print (np.dot(A, b))
# array([2, 2])