import csv

def check_column_count():
	with open('./raw_merged.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		count = 1

		ref_col_count = 0
		for row in rows:
			# print row
			# skip title line
			if 'Count_CellsFromBodipy' in row and ref_col_count == 0:
				ref_col_count = len(row)
			else:
				if len(row) != ref_col_count:
					print 'expected:{0} get:{1} rowID: {2}'.format(ref_col_count, len(row), count)

			count += 1


if __name__ == '__main__':
	check_column_count()