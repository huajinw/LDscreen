import csv

def shrink_pca_result():
	with open('./pca_result_20.csv', 'rU') as csvfile:
		with open('./pca_minimized.csv', 'w') as output:
			rows = csv.reader(csvfile)
			data_writer = csv.writer(output)
			for row in rows:
				new_row = row[:6]
				data_writer.writerow(new_row)

def check_shrink():
	with open('./pca_result_20.csv', 'rU') as csvfile:
		with open('./pca_minimized.csv', 'rU') as output:
			rows_1 = csv.reader(csvfile)
			rows_2 = csv.reader(output)
			for i in xrange(0, 438928):
				data_1 = rows_1.next()
				data_2 = rows_2.next()
				assert data_1[:6] == data_2

if __name__ == '__main__':
	shrink_pca_result()
	check_shrink()
