import csv

def get_layout_gene_info():

	pos_to_gene = {}

	with open('./raw_Genes.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			# skip title line
			if "PlateID" in row:
				continue

			assert len(row) == 3

			plat_num = row[0]
			assert '0000' in plat_num
			plat_num = plat_num.replace('0000', '')
			plat_num = plat_num.upper()

			well_num = row[1]
			well_num = well_num.upper()
			assert len(well_num) == 4
			assert ord('A') <= ord(well_num[0]) <= ord('Z')

			gene_name = row[2]
			gene_name = gene_name.strip().upper()

			combined_pos = plat_num + "_" + well_num
			assert combined_pos not in pos_to_gene

			pos_to_gene[combined_pos] = gene_name
	
	return pos_to_gene


def read_sample_data():
	layout_info = get_layout_gene_info()

	print 'get layout info completed'

	gene_to_data = {}

	negative_control = []
	positive_control_1 = []
	positive_control_2 = []

	missing = []


	with open('./raw_merged.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		count = 1

		for row in rows:

			if count % 10000 == 0:
				print 'finished processing ' + str(count) + ' rows'

			# skip title line
			if 'Count_CellsFromBodipy' in row:
				continue

			image_name_col = -3
			assert '.flex' in row[image_name_col]

			image_full_name = row[image_name_col]
			components = image_full_name.split('/')

			PlateID = components[-2]
			PlateID = PlateID.upper()
			wellID = components[-1].split('.')[0]

			assert '000' in wellID
			assert 'PY' in PlateID

			PlateID = PlateID.replace('PY0000', 'PY')
			assert len(PlateID) == 6
			assert len(wellID) == 9

			wellID = wellID[0:6]

			row_num = wellID[0:3]
			row_id = chr(int(row_num) - 1 + 65)
			wellID = row_id + wellID[3:6]
			assert len(wellID) == 4

			combined_pos = PlateID + '_' + wellID

			col_num = int(wellID[1:])
			if col_num not in [1, 2, 23, 24]:
				if combined_pos not in layout_info:
					missing.append(row)
					continue

				gene_name = layout_info[combined_pos]

				if gene_name not in gene_to_data:
					gene_to_data[gene_name] = [row]
				else:
					gene_to_data[gene_name].append(row)
			elif col_num in [1,2,23] and int(row_num) % 2 == 0:
				negative_control.append(row)
			elif int(row_num) % 2 == 1 and col_num == 1:
				positive_control_1.append(row)
			elif int(row_num) % 2 == 1 and col_num in [2,23]:
				positive_control_2.append(row)

			count += 1

	with open('grouped_data.csv', 'w') as csvfile:
		data_writer = csv.writer(csvfile)
		with open('gene_num.txt', 'w') as position_file:
			start = 0
			end = 0
			for gene_name, data_of_gene in gene_to_data.iteritems():
				for single_data in data_of_gene:
					data_writer.writerow(single_data)
					end += 1
				position_file.write('{0} {1} {2}\n'.format(gene_name, start, end - 1))
				start = end


	with open('negative.csv', 'w') as csvfile:
		data_writer = csv.writer(csvfile)
		for data_of_gene in negative_control:
			data_writer.writerow(data_of_gene)

	with open('pos_1.csv', 'w') as csvfile:
		data_writer = csv.writer(csvfile)
		for data_of_gene in positive_control_1:
			data_writer.writerow(data_of_gene)

	with open('pos_2.csv', 'w') as csvfile:
		data_writer = csv.writer(csvfile)
		for data_of_gene in positive_control_2:
			data_writer.writerow(data_of_gene)

	if missing:
		with open('missing.csv', 'w') as csvfile:
			data_writer = csv.writer(csvfile)
			for missing_data in missing:
				data_writer.writerow(missing_data)


if __name__ == '__main__':
	read_sample_data()