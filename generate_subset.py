import os
import csv
import pandas as pd
import random


def get_subset(filename):
	f = filename
	num_lines = sum(1 for l in open(f))
	print(num_lines)

	# randomly sample 1% of the data and store the kept indecis
	size = int(num_lines / 100)
	keep_idx = random.sample(range(num_lines), size)
	print(len(keep_idx))

	# find skipped index
	skip_idx = [i for i in range(num_lines) if i not in keep_idx] 
	print(len(skip_idx))

	df = pd.DataFrame(keep_idx)
	df.to_csv('keep_idx_%s' %filename, index=False, header=False)

	# Read the 1% subset and store in csv
	data = pd.read_csv(f, skiprows=skip_idx)
	print(data.shape)
	data.to_csv('subset_%s' %filename, index=False, header=False)

get_subset('outnormalize.csv')



