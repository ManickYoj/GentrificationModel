from __future__ import division
import json
import itertools
import math
from pprint import pprint

class State:
	"""docstring for ClassName"""
	def __init__(self, initialPosition):
		# self.poverty = initialPosition[0]
		# self.income = initialPosition[1]
		# self.home = initialPosition[2]
		# self.rent = initialPosition[3]
		# self.housing = initialPosition[4]
		self.params = initialPosition
		self.neighborhoods = []

	def getNewCenter(self):
		tempParams = [0]*len(self.params)
		tempLen = [0]*len(self.params) # because of null data
		for n in self.neighborhoods:
			for i in range(len(self.params)):
				if b[i] in n:
					if n[b[i]] is not None:
						tempParams[i] += int(n[b[i]])
						tempLen[i] += 1
		for i in range(len(self.params)):
			tempParams[i] /= tempLen[i]
			tempParams[i] = int(tempParams[i])
		self.params = tempParams[:]

def calculateDistance(neighborhood, state):
	distance = 0
	for i in range(num_values):
		if b[i] in neighborhood:
			if neighborhood[b[i]] is not None:
				sub = int(neighborhood[b[i]])-state.params[i]
				normalize = sub/(amax[i]-amin[i])
				square = normalize**2
				distance += square
	distance = math.sqrt(distance)
	# print "distance: " + str(distance)
	return distance

def findClosestCentroid(neighborhood, centroids):
	min_distance = float("inf")
	closestState = centroids[0]
	for state in centroids:
		if calculateDistance(neighborhood, state) < min_distance:
			min_distance = calculateDistance(neighborhood, state)
			closestState = state
			# print "min_distance: " + str(min_distance)
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
for i in range(len(data)):
	if 'Housing Units' in data[i]:
		if data[i]['Housing Units'] is not None:
			if int(data[i]['Housing Units']) > max_housing:
				max_housing = int(data[i]['Housing Units'])
	if 'Impoverished Pop' in data[i]:
		if data[i]['Impoverished Pop'] is not None:
			if int(data[i]['Impoverished Pop']) > max_poverty:
				max_poverty = int(data[i]['Impoverished Pop'])
	if 'Median Contract Rent' in data[i]:
		if data[i]['Median Contract Rent'] is not None:
			if int(data[i]['Median Contract Rent']) > max_rent:
				max_rent = int(data[i]['Median Contract Rent'])
	if 'Median Home Value' in data[i]:
		if data[i]['Median Home Value'] is not None:
			if int(data[i]['Median Home Value']) > max_home:
				max_home = int(data[i]['Median Home Value'])
	if 'Median Household Income' in data[i]:
		if data[i]['Median Household Income'] is not None:
			if int(data[i]['Median Household Income']) > max_income:
				max_income = int(data[i]['Median Household Income'])

# Calculate min
	if 'Housing Units' in data[i]:
		if int(data[i]['Housing Units']) < min_housing:
			if data[i]['Housing Units'] is not None:
				min_housing = int(data[i]['Housing Units'])
	if 'Impoverished Pop' in data[i]:
		if data[i]['Impoverished Pop'] is not None:
			if int(data[i]['Impoverished Pop']) < min_poverty:
				min_poverty = int(data[i]['Impoverished Pop'])
	if 'Median Contract Rent' in data[i]:
		if data[i]['Median Contract Rent'] is not None:
			if int(data[i]['Median Contract Rent']) < min_rent:
				min_rent = int(data[i]['Median Contract Rent'])
	if 'Median Home Value' in data[i]:
		if data[i]['Median Home Value'] is not None:
			if int(data[i]['Median Home Value']) < min_home:
				min_home = int(data[i]['Median Home Value'])
	if 'Median Household Income' in data[i]:
		if data[i]['Median Household Income'] is not None:
			if int(data[i]['Median Household Income']) < min_income:
				min_income = int(data[i]['Median Household Income'])

#print max(int(feature["Median Home Value"]) for feature in data)

## We are assuming min values for all characteritics are 0

amax = [max_poverty, max_income, max_home, max_rent, max_housing]
amin = [min_poverty, min_income, min_home, min_rent, min_housing]
print "max: " + str(amax)
print "min: " + str(amin)
# point_list = [amin, amax, [min_poverty, max_income, min_home]]#, min_rent, max_housing]]
# print "point_list: " + str(point_list)
b = ['Housing Units', 'Impoverished Pop', 'Median Contract Rent', 'Median Home Value', 'Median Household Income']

# #set one index in a to 0
# for i in range(k-2):
# 	params = amax[:]
# 	if i < num_values:
# 		params[i] = amin[i]
# 		point_list.append(params)
# 		# a = [max_poverty, max_income, max_home, max_rent, max_housing]


# # #set 2 indices in a to 0
# doubles = list(itertools.combinations(range(0,num_values), 2))
# for tuple in doubles:
# 	params = amax[:]
# 	if (len(point_list) < k):
# 		params[tuple[0]] = amin[tuple[0]]
# 		params[tuple[1]] = amin[tuple[1]]
# 		point_list.append(params)
		# amax = [max_poverty, max_income, max_home, max_rent, max_housing]

# start centriods based on the first points
# assuming that first k points are good data
point_list = []
i = 0
params1 = [0]*num_values
while len(point_list) < k:
	append = True
	params = params1[:] # we need copies of the object
	for j in range(num_values):
		if 'Median Contract Rent' in data[i]:
			if data[i]['Median Contract Rent'] is not None:
				params[j] = int(data[i][b[j]])
			else:
				append = False
	if append:
		point_list.append(params)
	i+=1

states = []
for point in point_list:
	states.append(State(point))


for neighborhood in data:
	state = findClosestCentroid(neighborhood, states)
	state.neighborhoods.append(neighborhood)

for c in states:
	# if (len(c.neighborhoods) == 0):
	print len(c.neighborhoods)
	# print c.params
# print states[12].params

## Move the centroids
for c in states:
	c.getNewCenter()

print "MOVE CENTROIDS"
# for c in states:
# 	print c.params

for neighborhood in data:
	state = findClosestCentroid(neighborhood, states)
	state.neighborhoods.append(neighborhood)

for c in states:
# if (len(c.neighborhoods) == 0):
	print len(c.neighborhoods)
# print c.params
# print states[12].params