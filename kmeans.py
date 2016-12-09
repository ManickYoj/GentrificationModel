import json
import itertools
import math
from pprint import pprint

class State:
	"""docstring for ClassName"""
	def __init__(self, initialPosition):
		self.poverty = initialPosition[0]
		self.income = initialPosition[1]
		self.home = initialPosition[2]
		self.rent = initialPosition[3]
		self.housing = initialPosition[4]
		self.neighborhoods = []

def calculateDistance(neighborhood, state):
	distance = 0
	for i in range(num_values):
		if b[i] in neighborhood:
			if neighborhood[b[i]] is not None:
				distance += int(neighborhood[b[i]])
	distance = math.sqrt(distance)
	return distance

def findClosestCentroid(neighborhood, centroids):
	min_distance = float("inf")
	closestState = centroids[0]
	for state in centroids:
		if calculateDistance(neighborhood, state) < min_distance:
			min_distance = calculateDistance(neighborhood, state)
			closestState = state
	# print closestState
	return closestState


with open('data.json') as data_file:
	data = json.load(data_file)


k = 18 #number of k clusters
num_values = 5  #number of characteristics we are clustering with
max_housing = 999
max_poverty = 992
max_rent = 996
max_home = 963300
max_income = 99615
min_housing = data[0]['Housing Units']
min_poverty = data[0]['Impoverished Pop']
min_rent = data[0]['Median Contract Rent']
min_home = data[0]['Median Home Value']
min_income =data[0]['Median Household Income']
# min_housing = data[0]['Housing Units']
# min_poverty = data[0]['Impoverished Pop']
# min_rent = data[0]['Median Contract Rent']
# min_home = data[0]['Median Home Value']
# min_income =data[0]['Median Household Income']

## The following code was used to determine max values
# for i in range(len(data)):
# 	if 'Housing Units' in data[i]:
# 		if data[i]['Housing Units'] > max_housing:
# 			max_housing = data[i]['Housing Units']
# 	if 'Impoverished Pop' in data[i]:
# 		if data[i]['Impoverished Pop'] > max_poverty:
# 			max_poverty = data[i]['Impoverished Pop']
# 	if 'Median Contract Rent' in data[i]:
# 		if data[i]['Median Contract Rent'] > max_rent:
# 			max_rent = data[i]['Median Contract Rent']
# 	if 'Median Home Value' in data[i]:
# 		if data[i]['Median Home Value'] > max_home:
# 			max_home = data[i]['Median Home Value']
# 	if 'Median Household Income' in data[i]:
# 		if data[i]['Median Household Income'] > max_income:
# 			max_income = data[i]['Median Household Income']

# Calculate min
# for i in range(len(data)):
# 	if 'Housing Units' in data[i]:
# 		if data[i]['Housing Units'] < min_housing:
# 			if data[i]['Housing Units'] is not None:
# 				min_housing = data[i]['Housing Units']
# 	if 'Impoverished Pop' in data[i]:
# 		if data[i]['Impoverished Pop'] is not None:
# 			if data[i]['Impoverished Pop'] < min_poverty:
# 				min_poverty = data[i]['Impoverished Pop']
# 	if 'Median Contract Rent' in data[i]:
# 		if data[i]['Median Contract Rent'] is not None:
# 			if data[i]['Median Contract Rent'] < min_rent:
# 				min_rent = data[i]['Median Contract Rent']
# 	if 'Median Home Value' in data[i]:
# 		if data[i]['Median Home Value'] is not None:
# 			if data[i]['Median Home Value'] < min_home:
# 				print min_home
# 				min_home = data[i]['Median Home Value']
# 				print min_home
# 	if 'Median Household Income' in data[i]:
# 		if data[i]['Median Household Income'] is not None:
# 			if data[i]['Median Household Income'] < min_income:
# 				min_income = data[i]['Median Household Income']

print max(feature["Median Home Value"] for feature in data)

## We are assuming min values for all characteritics are 0
point_list = [[0, 0, 0, 0, 0], [max_poverty, max_income, max_home, max_rent, max_housing], [0, max_income, 0, 0, max_housing]]
a = [max_poverty, max_income, max_home, max_rent, max_housing]
amin = [min_poverty, min_income, min_home, min_rent, min_housing]
print amin

b = ['Housing Units', 'Impoverished Pop', 'Median Contract Rent', 'Median Home Value', 'Median Household Income']

#set one index in a to 0
for i in range(k-2):
	if i < 5:
		a[i] = 0
		point_list.append(a)
		a = [max_poverty, max_income, max_home, max_rent, max_housing]

#set 2 indices in a to 0
doubles = list(itertools.combinations([0, 1, 2, 3, 4], 2))
for tuple in doubles:
	a[tuple[0]] = 0
	a[tuple[1]] = 0
	point_list.append(a)
	a = [max_poverty, max_income, max_home, max_rent, max_housing]

states = []
for point in point_list:
	states.append(State(point))


for neighborhood in data:
	state = findClosestCentroid(neighborhood, states)
	state.neighborhoods.append(neighborhood)

