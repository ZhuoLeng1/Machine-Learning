import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

import bs4
import json
import sys
import csv
import json
import time 
import requests


'''
-----------------------------------------------------------------------------------------
Problem 1 Data Acquisition and Analysis
-----------------------------------------------------------------------------------------
'''

##question 1

##import data
graffiti = pd.read_csv('Graffiti_Removal.csv')

pot = pd.read_csv('Pot_Holes_reported.csv', names =['Creation Date', 'Status', 'Completion Date', 'Service Request Number',
       'Type of Service Request', 'Current Activity',
       'Most Recent Action', 'Number of Potholes Filled On Block', 'Street Address', 'ZIP Code',
       'X Coordinate', 'Y Coordinate', 'Ward', 'Police District',
       'Community Area', 'SSA', 'Latitude', 'Longitude', 'Location'], skiprows = [0])

sanitation = pd.read_csv('Sanitation_Code_Complaints.csv', skiprows = [1])

vacant = pd.read_csv('Vacant_and_Abandoned_Buildings_Reported.csv',
	names = ['Type of Service Request', 'Service Request Number', 'Creation Date',
       'Location of Building on the lot', 'Is the Building Dangerous or Hazarous?',
       'Is Building Open Or Board?', 'IF THE BUILDING IS OPEN, WHERE IS THE ENTRY POINT?',
       'IS THE BUILDING CURRENTLY VACANT OR OCCUPIED?', 'IS THE BUILDING VACANT DUE TO FIRE?',
       'ANY PEOPLE USING PROPERTY? (HOMELESS, CHILDEN, GANGS)', 
       'ADDRESS STREET NUMBER', 'ADDRESS STREET DIRECTION',
       'ADDRESS STREET NAME', 'ADDRESS STREET SUFFIX', 'ZIP Code',
       'X Coordinate', 'Y Coordinate', 'Ward', 'Police District',
       'Community Area', 'Latitude', 'Longitude', 'Location'], skiprows = [0,1])

## question 2

'''
-----------------------------------------------------------------------------------------
Help function
-----------------------------------------------------------------------------------------
'''

#### figure and table of total number of request by the four different 311 requests
def main_type_by_year():
	'''
	Input a datafram(string format) and get the summary statistics and the bar chat plot for this main type
	311 request from year 2011 to 2016

	Input:
	'graffiti' or 'pot' or 'sanitation'

	Output:
	summary statistics of certain types 311 request by years(2011-2016) under input df types

	'''

	graffiti['year'] = graffiti['Creation Date'].apply(lambda x: x[-4:])
	grouped_graffiti = (graffiti.groupby('year').size())
	#only get the amount from 2011 to 2016
	amount_graffiti = grouped_graffiti[-7:-1]


	pot['year'] = pot['Creation Date'].apply(lambda x: x[-4:])
	grouped_pot = pot.groupby('year').size()
	#only get the amount from 2011 to 2016
	amount_pot = grouped_pot[-7:-1]

	sanitation['year'] = sanitation['Creation Date'].apply(lambda x: x[-4:])
	grouped_sanitation = sanitation.groupby('year').size()
	#only get the amount from 2011 to 2016
	amount_sanitation = grouped_sanitation[-7:-1]


	vacant['year'] = vacant['Creation Date'].apply(lambda x: x[-4:])
	grouped_vacant = vacant.groupby('year').size()
	#only get the amount from 2011 to 2016
	amount_vacant = grouped_vacant[-7:-1]

	df =  pd.concat([amount_graffiti, amount_pot, amount_sanitation, amount_vacant],axis=1)
	df = df.rename(index=str, columns={0: "amount_graffiti", 1: "amount_pot", 2: 'amount_sanitation', 3: 'amount_vacant'})

	##plot
	fig, ax = plt.subplots(figsize =(8,8))
	plt.plot(df.index, df.amount_graffiti, marker = 'D',label = 'amount of graffiti removal request')
	plt.plot(df.index, df.amount_pot, marker = 'o',label = 'amount of pot hole request')
	plt.plot(df.index, df.amount_sanitation, marker ='o', color = 'b',label = 'amount of sanitation request')
	plt.plot(df.index, df.amount_vacant, marker = 'D', color = 'maroon',label = 'amount of vacant request')

	plt.title('311 requests amounts from 2011 to 2016', fontsize=20)
	plt.xlabel(r'year')
	plt.ylabel(r'amount of 311 request')
	plt.legend(loc='upper right')

	#plt.show()
	plt.close()

	return df


#number of requests of subtypes
def subtype_request(df):
	'''
	Input a datafram(string format) and get the summary statistics and the bar chat plot of each subtypes 
	under this main type.

	Input:
	'graffiti' or 'pot' or 'sanitation'

	Output:

	summary statistics of each types under the input datafram
	'''

	if df == 'graffiti':
		grouped_1 = graffiti.groupby('What Type of Surface is the Graffiti on?').size().order(ascending=False).head(5)
		grouped_2 = graffiti.groupby('Where is the Graffiti located?').size().order(ascending=False).head(5)
		grouped_3 = graffiti.groupby('Community Area').size().order(ascending=False).head(5)
		grouped_4 = graffiti.groupby('response time(days)').size().order(ascending=False).head(5)
		

	elif df == 'pot':
		grouped_1 = pot.groupby('Current Activity').size().order(ascending=False).head(5)
		grouped_2 = pot.groupby('Number of Potholes Filled On Block').size().order(ascending=False).head(5)
		grouped_3 = pot.groupby('Community Area').size().order(ascending=False).head(5)
		grouped_4 = pot.groupby('response time(days)').size().order(ascending=False).head(5)

	elif df == 'sanitation':
		grouped_1 = sanitation.groupby('What is the Nature of this Code Violation?').size().order(ascending=False).head(5)
		grouped_2 = sanitation.groupby('Status').size().order(ascending=False).head(5)
		grouped_3 = sanitation.groupby('Community Area').size().order(ascending=False).head(5)
		grouped_4 = sanitation.groupby('response time(days)').size().order(ascending=False).head(5)

	fig = plt.figure(figsize = (10,10))

	ax1 = fig.add_subplot(2, 2, 1)
	ax1.title.set_text('{}'.format(grouped_1.index.name))
	grouped_1.plot(kind = 'bar')

	ax2 = fig.add_subplot(2, 2, 2)
	ax2.title.set_text('{}'.format(grouped_2.index.name))
	grouped_2.plot(kind = 'bar')

	ax3 = fig.add_subplot(2, 2, 3)
	ax3.title.set_text('{}'.format(grouped_3.index.name))
	grouped_3.plot(kind = 'bar')

	ax4 = fig.add_subplot(2, 2, 4)
	ax4.title.set_text('{}'.format(grouped_4.index.name))
	grouped_4.plot(kind = 'bar')
	#plt.show()
	plt.close()

	return grouped_1, grouped_2, grouped_3, grouped_4



#over time
def response_time(df):
	'''
	Input a dataframe and add columns of response time(days) depends on completion date and
	creation date

	Input:
	dataframe

	'''
	date_format = "%m/%d/%Y"

	lst_completion = []
	for i in df['Completion Date']:
		if isinstance(i, str):
			dt = datetime.strptime(i, date_format)
		else:
			dt = np.nan

		lst_completion.append(dt)

	lst_creation = []
	for i in df['Creation Date']:
		if isinstance(i, str):
			dt = datetime.strptime(i, date_format)
		else:
			dt = np.nan
		
		lst_creation.append(dt)

	days = np.zeros(len(lst_completion))
	for i in range(len(lst_completion)):
		if isinstance(lst_completion[i], float) or isinstance(lst_creation[i], float):
			days[i] = -1
		else:
			days[i] = (lst_completion[i] - lst_creation[i]).days
		
	df['response time(days)'] = days

	return


##update the response time of the first three dataframe
response_time(graffiti)
response_time(pot)
response_time(sanitation)

##number of request in each subtypes including response time
sub_graffiti = subtype_request('graffiti')
sub_pot = subtype_request('pot')
sub_sanitation = subtype_request('sanitation')


## figure and table of total number of request by the four different 311 requests using total data
fig = plt.figure()
dic_total_request = {'graffiti':len(graffiti), 'pot':len(pot), 'sanitation':len(sanitation), 'vacant':len(vacant)}
df_total_request = pd.Series(dic_total_request).to_frame('number of request')
df_total_request.plot(kind = 'bar')
#plt.show()
plt.close()

#after groupby year(2011-2016), figure out the relationship among four type of requests.
df = main_type_by_year()

'''
-----------------------------------------------------------------------------------------
Problem 2: Data Augmentation and APIs
-----------------------------------------------------------------------------------------
'''

def get_census(dataframe):
	'''
	Use lat and lon of dataframe to get fips number and use fips number to make a call to get
    census api

	Input: dataframe

	Output: dataframe
	'''

	df = dataframe[(dataframe['year'] == '2017')].reset_index(drop = True)
	df = df.dropna(subset = [['Latitude','Longitude']]).reset_index(drop = True)

	lat = df['Latitude']
	lon = df['Longitude']

	B01001F_001E = []
	B19119_001E = []
	B05010_001E = []

	for i in range(len(lat)):

		#first use lat and lon to get fips data
		api_url = 'http://data.fcc.gov/api/block/find?format=json&latitude={}&longitude={}&showall=true'.format(lat[i], lon[i])
		r = requests.get(api_url)
		soup = bs4.BeautifulSoup(r.text, 'lxml') 
		fips = json.loads(soup.text)

		state = fips['State']['FIPS']
		county = fips['County']['FIPS'][2:]
		tract = fips['Block']['FIPS'][5:-4]
		block = fips['Block']['FIPS'][-4:]

		#then use fips data to call census api
		new_url = 'http://api.census.gov/data/2014/acs5?get=B01001F_001E,B19119_001E,B05010_001E&for=tract:{}&in=state:{}+county:{}&key=def7402f5045a06a516edc0f1e774d6155b11eb2'.format(tract, state, county)

		r = requests.get(new_url)
		soup = bs4.BeautifulSoup(r.text, 'lxml') 
		census = json.loads(soup.text)[1]

		B01001F_001E.append(census[0])
		B19119_001E.append(census[1])
		B05010_001E.append(census[2])

	df['B01001F_001E'] = B01001F_001E
	df['B19119_001E'] = B19119_001E
	df['B05010_001E'] = B05010_001E

	return df


census_sanitation = get_census(sanitation)
census_vacant = get_census(vacant)

#1.What types of blocks get “Vacant and Abandoned Buildings Reported”?
census_vacant['B19119_001E'].astype(float).describe()
census_vacant['B05010_001E'].astype(float).describe()

#2.What types of blocks get “Sanitation Code Complaints”?
census_sanitation['B01001F_001E'].astype(float).describe()
census_sanitation['B19119_001E'].astype(float).describe()
census_sanitation['B05010_001E'].astype(float).describe()

#3.Does that change over time in the data you collected?
census_sanitation['B01001F_001E'] = census_sanitation['B01001F_001E'].astype(float)
census_sanitation['B19119_001E'] = census_sanitation['B19119_001E'].astype(float)
census_sanitation['B05010_001E'] = census_sanitation['B05010_001E'].astype(float)

census_vacant['B01001F_001E'] = census_vacant['B01001F_001E'].astype(float)
census_vacant['B19119_001E'] = census_vacant['B19119_001E'].astype(float)
census_vacant['B05010_001E'] = census_vacant['B05010_001E'].astype(float)

#get the month data of each type of request
census_sanitation['month'] = census_sanitation['Creation Date'].apply(lambda x: x[:2])
census_vacant['month'] = census_vacant['Creation Date'].apply(lambda x: x[:2])

#groupby time
census_sanitation.groupby('month').mean()
census_sanitation.groupby('month').median()

census_vacant.groupby('month').mean()
census_vacant.groupby('month').median()

'''
-----------------------------------------------------------------------------------------
Problem 3
-----------------------------------------------------------------------------------------
'''

# question 1
address = '7500 S Wolcott Ave'

#From the address, we could know that the zip code of address is 60620
count_graffiti = len(graffiti[graffiti['ZIP Code'] == 60620.0])
count_pot = len(pot[pot['ZIP Code'] == 60620.0])
count_sanitation = len(sanitation[sanitation['ZIP Code'] == 60620.0])
count_vacant = len(vacant[vacant['ZIP Code'] == 60620.0])

total = count_graffiti + count_pot + count_vacant + count_sanitation
p_graffiti = count_graffiti/total
p_pot = count_pot/total
p_sanitation = count_sanitation/total
p_vacant = count_vacant/total

#question 2
#Because Lawndale is one of the community area of Chicago and it community area code is 30. 
#Uptown's community area code is 03.
count_graffiti_law = len(graffiti[graffiti['Community Area'] == 30.0])
count_graffiti_up = len(graffiti[graffiti['Community Area'] == 03.0])

total = count_graffiti_up + count_graffiti_law
dif = count_graffiti_law/total - count_graffiti_up/total


#question 3
p_eng = 100/600
p_uptown = 160/400
dif_2 = p_uptown - p_eng
