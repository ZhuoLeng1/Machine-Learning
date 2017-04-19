import pandas as pd
import pylab as pl
import numpy as np
import re

def read_data(filename):
	'''
	inpute csv file and output dataframe

	input: filename

	Output: dataframe
	'''
	df = pd.read_csv(filename)

	return df
