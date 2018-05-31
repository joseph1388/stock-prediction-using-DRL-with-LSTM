import numpy as np
def bornulli(p):
	return 1 if np.random.rand() > p else 0

def gaussian(mu, std):
	return np.random.normal(mu, std)