from sklearn.linear_model import LogisticRegression
import numpy as mp

def accuracy(lm, df, features, outcome_var):
	'''
	Explained variance score: 1 is perfect prediction
	and 0 means that there is no linear relationship
	between X and y.

	input:
	lm: linear_model
	df: dataframe
	features:List 
	outcome_var:a string

	Output:
	mean accuracy
	'''
	score = lm.score(df[features], df[outcome_var]) 

	return score

def mse(lm, df, features, outcome_var):
	'''
	generate mse to summarize the fit of the model

	input:
	lm: linear_model
	df: dataframe
	features:List 
	outcome_var:a string

	Output:
	mse
	'''
	expected = df[outcome_var]
	predicted = lm.predict(df[features])
	mse = np.mean((predicted-expected)**2)
	return mse