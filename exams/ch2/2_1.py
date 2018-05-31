import os
import time
import warnings
import numpy as np
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

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