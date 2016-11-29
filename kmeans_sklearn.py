import numpy as np
from sklearn.cluster import KMeans

pca_data = np.loadtxt('pca_minimized_17.csv',delimiter=',')
inertia_array = np.zeros(14)

for i in range(2,11):
	kmeans = KMeans(n_clusters=i, random_state=0, n_jobs=4).fit(pca_data)
	pca_kmeans_result = kmeans.labels_
	inertia_array[i-2] = kmeans.inertia_
	filename = 'pca_kmeans_result_k'+str(i) +'.csv'
	np.savetxt(filename, pca_kmeans_result)

print(inertia_array)
