import numpy as np
from sklearn.cluster import KMeans

pca_data = np.loadtxt('pca_result_20.csv',delimiter=',')

for i in range(2,11):
	kmeans = KMeans(n_clusters=i, random_state=0).fit(pca_data)
	pca_kmeans_result = kmeans.labels_
	filename = 'pca_kmeans_result_k'+str(i) +'.csv'
	np.savetxt(filename, pca_kmeans_result)


