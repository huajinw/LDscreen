import os
import csv
from sklearn import svm
import numpy as np
from sklearn import preprocessing

POS_1_LINE_COUNT = 9744
POS_2_LINE_COUNT = 19481
NEGATIVE_LINE_COUNT = 29232
SAMPLE_LINE_COUNT = 380471

pos_1_data = []
pos_2_data = []
negative_data = []
experiment_data = []


lines = []
with open('./pca_minimized.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			lines.append(np.array(map(lambda x: float(x), row)))

assert POS_1_LINE_COUNT + POS_2_LINE_COUNT + NEGATIVE_LINE_COUNT + SAMPLE_LINE_COUNT == len(lines)

print "Done reading data"

pos_1_data = lines[:POS_1_LINE_COUNT]
pos_2_data = lines[POS_1_LINE_COUNT : (POS_1_LINE_COUNT + POS_2_LINE_COUNT)]
negative_data = lines[(POS_1_LINE_COUNT + POS_2_LINE_COUNT) : (POS_1_LINE_COUNT + POS_2_LINE_COUNT + NEGATIVE_LINE_COUNT)]
experiment_data = lines[(POS_1_LINE_COUNT + POS_2_LINE_COUNT + NEGATIVE_LINE_COUNT):]

assert len(pos_1_data) == POS_1_LINE_COUNT
assert len(pos_2_data) == POS_2_LINE_COUNT
assert len(negative_data) == NEGATIVE_LINE_COUNT
assert len(experiment_data) == SAMPLE_LINE_COUNT

gene_line_info = open('./grouped_data/gene_num.txt', 'r')
lines = gene_line_info.readlines()

gene_to_data = {}
for line in lines:
	components = line.split()
	assert len(components) in [3, 4]
	row_start = int(components[-2])
	row_end = int(components[-1])
	gene_name = components[0] if len(components) == 3 else components[0] + ' ' + components[1]
	assert gene_name not in gene_to_data
	if gene_name == "SELS":
		assert row_end == len(experiment_data) - 1
	gene_to_data[gene_name] = np.array(experiment_data[row_start: row_end + 1])

total_genes_count = len(gene_to_data.keys())
print 'total {0} genes without control'.format(total_genes_count)

all_sample_genes = gene_to_data.keys()
all_sample_genes = ['positive_1'] * 10 + ['positive_2'] * 10 + ['negative'] * 10 + all_sample_genes

try_count = 10

distance_metric = [None] * try_count
for i in xrange(0, try_count):
	distance_metric[i] = [0.5] * try_count

print "Done initializing distance metric"


for i in xrange(0, try_count):
	print "processing row {0}".format(i)

	if 0 <= i <= 9:
		row_gene_name = 'positive_1' + str(i)
		row_gene_data = pos_1_data[21 * i : 21 * (i + 1)]
	elif 10 <= i <= 19:
		row_gene_name = 'positive_2' + str(i - 10)
		row_gene_data = pos_2_data[21 * (i - 10) : 21 * (i - 10 + 1)]
	elif 20 <= i <= 29:
		row_gene_name = 'negative_' + str(i - 20)
		row_gene_data = negative_data[21 * (i - 20) : 21 * (i - 20 + 1)]
	else:
		row_gene_name = all_sample_genes[i]
		row_gene_data = gene_to_data[row_gene_name]

	for j in xrange(0, try_count):
		if i == j:
			distance_metric[i][j] = 0.0
		else:
			if 0 <= j <= 9:
				col_gene_name = 'positive_1' + str(j)
				col_gene_data = pos_1_data[21 * j : 21 * (j + 1)]
			elif 10 <= j <= 19:
				col_gene_name = 'positive_2' + str(j - 10)
				col_gene_data = pos_2_data[21 * (j - 10) : 21 * (j - 10 + 1)]
			elif 20 <= j <= 29:
				col_gene_name = 'negative_' + str(j - 20)
				col_gene_data = negative_data[21 * (j - 20) : 21 * (j - 20 + 1)]
			else:
				col_gene_name = all_sample_genes[j]
				col_gene_data = gene_to_data[col_gene_name]
			
			X = [None] * (len(row_gene_data) +len(col_gene_data))
			Y = [1] * (len(row_gene_data) +len(col_gene_data))


			for k in xrange(0, len(row_gene_data)):
				X[k] = row_gene_data[k]
			k += 1
			for l in xrange(0, len(col_gene_data)):
				X[k + l] = col_gene_data[l]
				Y[k + l] = 0
			assert X[-1] is not None
			assert Y[-1] != 1
			X = preprocessing.scale(X)

			clf = svm.SVC(tol=float(1e-10), max_iter=float(1e6), kernel='linear')
			clf.fit(X, Y)


			accuracy = 0

			for k in xrange(0, len(row_gene_data)):
				if clf.predict([row_gene_data[k]])[0] == 1:
					accuracy += 1

			for k in xrange(0, len(col_gene_data)):
				if clf.predict([col_gene_data[k]])[0] == 0:
					accuracy += 1

			distance_metric[i][j] = accuracy * 1.0 / (len(row_gene_data) +len(col_gene_data))

with open('./svm_metric_gene_names.txt', 'w') as output_gene_name_file:
	for i in xrange(0, try_count):
		gene_name = all_sample_genes[i]
		output_gene_name_file.write('{0}\n'.format(gene_name))

with open('./svm_metric_result.csv', 'w') as output_distance:
	for i in xrange(0, try_count):
		for j in xrange(0, try_count):
			if j == try_count - 1:
				output_distance.write("{0}\n".format(distance_metric[i][j]))
			else:
				output_distance.write("{0},".format(distance_metric[i][j]))





