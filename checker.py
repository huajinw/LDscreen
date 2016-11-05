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


def check_pos1(layout_info):
	print 'checking positive control 1'
	with open('./grouped_data/pos_1.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
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
			assert wellID[0] in ['A', 'C', 'E', 'G', 'I', 'K', 'M', 'O']
			assert wellID[1:] == '001'
			combined_pos = PlateID + '_' + wellID
			assert combined_pos not in layout_info


def check_pos2(layout_info):
	print 'checking positive control 2'
	with open('./grouped_data/pos_2.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
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
			assert wellID[0] in ['A', 'C', 'E', 'G', 'I', 'K', 'M', 'O']
			assert wellID[1:] == '002' or wellID[1:] == '023' 
			combined_pos = PlateID + '_' + wellID
			assert combined_pos not in layout_info


def check_negative(layout_info):
	print 'checking negative control'
	with open('./grouped_data/negative.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
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
			assert wellID[0] in ['B', 'D', 'F', 'H', 'J', 'L', 'N', 'P']
			assert wellID[1:] in ['001', '002', '023'] 
			combined_pos = PlateID + '_' + wellID
			assert combined_pos not in layout_info


def check_missing_data(layout_info):
	print 'checking missing data'
	with open('./grouped_data/missing.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
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
			assert wellID[1:] not in ['001', '002', '023'] 
			assert ord('A') <= ord(wellID[0]) <= ord('P') 
			combined_pos = PlateID + '_' + wellID
			assert combined_pos not in layout_info


def check_sample_data(layout_info):
	print 'checking sample data'

	current = None
	gene_line_info = []

	with open('./grouped_data/gene_num.txt', 'r') as line_data:
		lines = line_data.readlines()
		for line in lines:
			gene_line_info.append(line)


	with open('./grouped_data/grouped_data.csv', 'rU') as csvfile:
		rows = csv.reader(csvfile)
		current_index = 0
		for single_gene_info in gene_line_info:
			while current_index <= int(single_gene_info.split()[-1]):
				row = rows.next()
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
				assert wellID[1:] not in ['001', '002', '023'] 
				assert ord('A') <= ord(wellID[0]) <= ord('P') 
				combined_pos = PlateID + '_' + wellID
				assert combined_pos in layout_info
				gene_name = layout_info[combined_pos]
				assert gene_name in single_gene_info
				current_index += 1


if __name__ == '__main__':
	layout_info = get_layout_gene_info()
	check_sample_data(layout_info)
	check_negative(layout_info)
	check_pos1(layout_info)
	check_pos2(layout_info)
	check_missing_data(layout_info)