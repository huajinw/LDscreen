import numpy as np
from scipy.spatial.distance import pdist
import time

dataset = np.loadtxt('pca_minimized_17.csv',delimiter=',')
MAX_ITER = 100;

def kmeans(data, k, metric_type):
	#initalize
	numFeatures = data.shape[1]
	centroids = getRandomCentroids(numFeatures, k)
	iterations = 0
	oldCentroids = getRandomCentroids(numFeatures, k)
	
	while not should_stop(oldCentroids, centroids, iterations):
		oldCentroids = centroids
		iterations += 1
		labels = getLabels(data, centroids,metric_type)
		centroids = getCentroids(data, labels, k, numFeatures)
		print(iterations)
		print(np.linalg.norm(oldCentroids-centroids,ord = 'fro'))
	
	outputstring = 'k_'+ str(k) + '_' + str(metric_type) + '_'
	np.savetxt(outputstring+'centroids.txt', centroids, delimiter=',')
	np.savetxt(outputstring+'labels.txt', labels, delimiter=',')
	
		
def should_stop(oldCentroids, centroids, iterations):
	if iterations > MAX_ITER: 
		return True
	if (np.linalg.norm(oldCentroids-centroids, ord = 'fro') < 4):
		return True
	return False
	
def getLabels(data, centroids, metric_type):
	label_list = np.zeros(len(data))
	for i in range(len(data)):
		pair = np.array([data[i], centroids[0]])
		old_distance = pdist(pair, metric_type)
		label = 0;
		for j in range(len(centroids)):
			pair = np.array([data[i], centroids[j]])
			distance = pdist(pair, metric_type)
			if old_distance > distance:
				label = j
		label_list[i] = label
	return label_list

def getCentroids(data, labels, k, numFeatures):
	col_num = data.shape[1]
	Sum = np.zeros([k, col_num])
	for i in range(k):
		index_k = np.where(labels == i)[0]
		#print(len(index_k))
		#if len(index_k) == 0:
			#Sum[i] = np.random.normal(0,0,(1,numFeatures)) 
			#if there is not point in the current cluster, randomize the 
			#centroids
		#	break
		Sum[i] = np.sum(data[index_k], axis = 0) /(len(index_k))
		#Sum[i] = np.nan_to_num(Sum[i])
	return Sum #Sum is a storage matrix for centroids.

	
def getRandomCentroids(numFeatures, k):
	centroids = np.random.normal(0,1,(k,numFeatures))
	return centroids
	
if __name__ == '__main__':
	k = 4
	start_time = time.time()
	kmeans(dataset, k, 'euclidean')
	print("--- %s seconds ---" % (time.time() - start_time))


# Metric can be chosen from: 
# 'cityblock', 'correlation',
# 'cosine', 'euclidean', 'canberra', 'braycurtis'
	

	
	
	
	










