import pandas as pd


def print_null_freq(df):
    """
    for a given DataFrame, calculates how many values for 
    each variable is null and prints the resulting table to stdout
    """
    df_lng = pd.melt(df)
    null_variables = df_lng.value.isnull()
    return pd.crosstab(df_lng.variable, null_variables)
    

def fill_na(method,df,var):
	'''
	fill na with different method: mean/median/mod
	update dataframe

	Input:
	method: mean/median/mod
	df:DataFrame
	var:string(variable name)

	return:
	df[var]

	'''
	if method == 'mean':
		df[var] = df[var].fillna(df[var].mean())
	elif method == 'median':
		df[var] = df[var].fillna(df[var].median())


	return df[var]
