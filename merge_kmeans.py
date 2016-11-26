import numpy as np



data = np.loadtxt('pca_kmeans_result_k%d.csv' %2)
data = data.reshape((len(data),1))
print(data.shape)
for k in range(3, 11):
	a = np.loadtxt('pca_kmeans_result_k%d.csv' %k)
	a = a.reshape((len(data),1))
	print(a.shape)
	data = np.hstack((data,a))
print(data.shape)
np.savetxt('kmeans_2-10.txt', data, fmt='%i', delimiter=' ')