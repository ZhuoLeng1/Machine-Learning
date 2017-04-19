from sklearn.linear_model import LogisticRegression
import pylab as pl

def logistic_regression(df, features, outcome_var):
	'''
	generate logistic regression model.

	Input:
	df: dataframe
	features: list of varibale name
	outcome: a string:variable name

	Output:
	model
	'''

	lm = LogisticRegression()

	lm.fit(df[features], df[outcome_var])

	return lm


def plot_pred_actual(df, features, outcome_var):
	'''
	Plot the predicted values against the actual values

	Input:
	df: dataframe
	features: list of varibale name
	outcome: a string:variable name

	'''
	# add actual vs. predicted points
	lm = LogisticRegression()
	lm.fit(df[features], df[outcome_var])

	pl.scatter(df[outcome_var], lm.predict(df[features]))
	# add the line of perfect fit
	straight_line = np.arange(0, 100)
	pl.plot(straight_line, straight_line)
	pl.title("Fitted Values")

	return