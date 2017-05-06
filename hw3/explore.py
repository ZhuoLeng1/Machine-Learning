import pandas as pd
import matplotlib.pyplot as plt



#describe the data
def number_count(df, var):
	'''
	generate variables number count top 10 and plot them out

	Input: 
	df
	variable

	output:
	table
	'''
	table = pd.value_counts(df[var], ascending=False).head(10)
	table.plot(kind = 'bar')

	return table

def crosstable(df, var1, var2):
	'''
	generate crosstale of var1 and var2, and plot them out

	'''
	ct = pd.crosstab(df[var], df[var2])
	ct.plot(figsize=(10,10))

	return ct
