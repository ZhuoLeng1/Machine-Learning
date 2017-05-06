import pandas as pd

def discretize_continuous_var(df,var,bin):
	'''
	discretize a continuous variable.
	update df

	input: 
	bin: interger
	dataframe
	string(continuous variable name)
	'''
	disc = pd.cut(df[var], bin)
	df = pd.concat([df, disc], axis=1)

	return disc


def categorical_var(df, var):
	'''
	take a categorical variable and create binary/dummy variables from it.
	update df

	input:
	dataframe
	string(categorical variable name)
	'''
	dummies = pd.get_dummies(df[var], prefix = var)
	df = pd.concat([df, dummies], axis=1)
	return dummies



