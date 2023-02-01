import pickle

import numpy as np

def array2probability(x, method="roulette_wheel", inverse=False):
	if method == "roulette_wheel":
		sort = np.argsort(x)
		index = np.argsort(sort)

		k = 4
		n = len(x)
		d = (k-1)/(n-1)

		if not inverse:
			probability = np.array([1+d*index[i] for i in range(n)])
		else:
			probability = np.array([1+d*(n-1-index[i]) for i in range(n)])
		probability = probability/sum(probability)

	elif method == "softmax":
		x = np.exp(x)
		probability = x/sum(x)
	
	return probability

def nan2zero(x):
	return np.nan_to_num(x, nan=0, posinf=0, neginf=0)

def loadPickle(path):
	with open(path, "rb") as f:
		data = pickle.load(f)
	return data
	
def savePickle(path, data):
	with open(path, "wb") as f:
		pickle.dump(data, f)   	