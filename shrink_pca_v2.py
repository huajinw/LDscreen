import csv
import numpy as np


pca = 40 	
pc_n = 17

filename = './pca_result_%d.csv' %pca
outfile = './pca_minimized_%d.csv' %pc_n

f = np.loadtxt(filename,delimiter=',')
print('shape', f.shape)

def shrink_pca_result():
	with open(filename, 'rU') as csvfile:
		with open(outfile, 'w') as output:
			rows = csv.reader(csvfile)
			data_writer = csv.writer(output)
			for row in rows:
				new_row = row[:pc_n]
				data_writer.writerow(new_row)


def check_shrink():
	with open(filename, 'rU') as csvfile:
		with open(outfile, 'rU') as output:
			rows_1 = csv.reader(csvfile)
			rows_2 = csv.reader(output)
			for i in range(f.shape[1]):
				data_1 = rows_1.__next__()
				data_2 = rows_2.__next__()
				assert data_1[:pc_n] == data_2

if __name__ == '__main__':
	shrink_pca_result()
	check_shrink()
