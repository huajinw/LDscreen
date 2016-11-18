import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

def preprocessor(filename):
	X = np.loadtxt(filename,delimiter=',')
	X = np.nan_to_num(X)
	output_name = 'out'+ filename
	Xscaled = preprocessing.scale(X)
	np.savetxt(output_name, Xscaled, delimiter=',')

preprocessor('post_pos_1.csv')
preprocessor('post_pos_2.csv')
preprocessor('post_negative.csv')
preprocessor('post_grouped_data.csv')	

	
	





 
