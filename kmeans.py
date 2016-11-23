import numpy as np
from scipy.spatial.distance import pdist

dataset = np.loadtxt('outnormalize.csv',delimiter=',')
MAX_ITER = 100;

def kmeans(data, k):
	#initalize
	numFeatures = data.shape[1]
	centroids = getRandomCentroids(numFeatures, k)
	iterations = 0
	oldCentroids = getRandomCentroids(numFeatures, k)
	
	while not should_stop(oldCentroids, centroids, iterations):
		oldCentroids = centroids
		iterations += 1
		labels = getLabels(data, centroids)
		centroids = getCentroids(data, labels, k)
		print(iterations)
		print(np.linalg.norm(oldCentroids-centroids,ord = 'fro'))
	
		
def should_stop(oldCentroids, centroids, iterations):
	if iterations > MAX_ITER: 
		return True
	if (np.linalg.norm(oldCentroids-centroids, ord = 'fro') < 0.01):
		return True
	return False
	
def getLabels(data, centroids):
	label_list = np.zeros(len(data))
	for i in range(len(data)):
		pair = np.array([data[i], centroids[0]])
		old_distance = pdist(pair, 'euclidean')
		label = 0;
		for j in range(len(centroids)):
			pair = np.array([data[i], centroids[j]])
			distance = pdist(pair, 'euclidean')
			if old_distance > distance:
				label = j
		label_list[i] = label
	return label_list

def getCentroids(data, labels, k):
	col_num = data.shape[1]
	Sum = np.zeros([k, col_num])
	for i in range(k):
		index_k = np.where(labels == i)[0]
		Sum[i] = np.sum(data[index_k], axis = 0) /(len(index_k))
		#Sum[i] = np.nan_to_num(Sum[i])
	return Sum #Sum is a storage matrix for centroids.

	
def getRandomCentroids(numFeatures, k):
	centroids = np.random.normal(0,1,(k,numFeatures))
	return centroids
	
	
kmeans(dataset, 2)


	

	
	
	
	










