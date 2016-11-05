import os

directory = '/Volumes/EHD3/MacrophageScreen_RawData/'

print(os.listdir(directory))
files = []

for folder in os.listdir(directory):
	file = directory + '/' + folder + '/' + "DefaultOUT_Image.csv"
	files.append(file)

des = open('/Users/Huajin/Huajin_files/701project/final.csv', 'w+')
for file in files:
	current = open(file)
	print(current)
	lines = current.readlines()
	for line in lines:
		des.write(line)
	current.close()
des.close()
