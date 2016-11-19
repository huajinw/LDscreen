import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

def preprocessor(filename):
	X = np.loadtxt(filename,delimiter=',')
	X = np.nan_to_num(X)
	output_name = 'out'+ filename
	Xscaled = preprocessing.scale(X)
	np.savetxt(output_name, Xscaled, delimiter=',')

preprocessor('normalize.csv')

	





 
