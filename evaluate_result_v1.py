import numpy as np

POS_1_LINE_COUNT = 9744
POS_2_LINE_COUNT = 19481
NEGATIVE_LINE_COUNT = 29232
SAMPLE_LINE_COUNT = 380471

start_k = 2
end_k = 10

data = np.loadtxt('kmeans_2-10.txt')

n_samples, n_features = data.shape
print(data.shape)
assert POS_1_LINE_COUNT + POS_2_LINE_COUNT + NEGATIVE_LINE_COUNT + SAMPLE_LINE_COUNT == data.shape[0]


for k in range(start_k,end_k+1): 
	data_k = data[:,k-2]

	predictions = dict()
	for label in range(k):
		predictions[label] = []


	for i in range(n_samples):
		if i <= POS_1_LINE_COUNT: 
			cat = 'pos1'
		elif POS_1_LINE_COUNT < i <= POS_2_LINE_COUNT:
			cat = 'pos2' 
		elif POS_2_LINE_COUNT < i <= NEGATIVE_LINE_COUNT:
			cat = 'neg'
		else:
			cat = 'unknown'
		label = data_k[i]
		predictions[label].append(cat) 

	print(len(predictions))
	print(len(predictions[0]))


	for label in range(k):
		count_pos1, count_pos2, count_neg, count_unknown = 0, 0, 0, 0
		
		for i in range(len(predictions[label])):
			if predictions[label][i] == 'pos1':
				count_pos1 += 1
			elif predictions[label][i] == 'pos2':
				count_pos2 += 1
			elif predictions[label][i] == 'neg':
				count_neg += 1
			else:
					count_unknown += 1
		print('k=',k, 'label=',label, 'pos1=',count_pos1,'pos2=',count_pos2, \
			'neg=',count_neg,'unknown=',count_unknown)












