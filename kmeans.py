from __future__ import division
import json
import itertools
import math
from pprint import pprint
from ConfigParser import SafeConfigParser

## Use these methods to create states (groups of neighborhoods) using k-means clustering
## This script assigns neighborhoods to each state at the starting time

## Class that holds groups of neighborhoods and the associated properties
class State:
	def __init__(self, initialPosition):
		# parameter values of the center of the state
		self.params = initialPosition
		# List of neighborhoods in this group (each neighborhood is a json object)
		self.neighborhoods = []
		# We want to stop moving the centroids of the states eventually
		# If parameters move less than 0.2% from the previous value, they have stopped 
		self.needsToMove = True # they all start out moving
		self.movePercent = 0.002 # threshold percentage

	## Update the center of the group based on neighborhoods in this state
	## Find the average for each parameter of the neighborhoods
	def getNewCenter(self, paramNames):

		self.needsToMove = False # will set to true later if still need to move

		# helper var for calculating new params
		tempParams = [0]*len(self.params) 
		# because of null data, we divide by the number of neighborhoods for each param
		tempLen = [0]*len(self.params) 

		# Loop through all the neighborhoods to get average
		for n in self.neighborhoods:
			# For each neighborhood, go through all parameters
			for i in range(len(self.params)):
				# Make sure param value is not null
				if paramNames[i] in n:
					if n[paramNames[i]] is not None:
						# Increase the total sum of the given parameter
						tempParams[i] += int(n[paramNames[i]])
						# Increment the number of neighborhoods that have contributed to this value
						tempLen[i] += 1
		for i in range(len(self.params)):
			# divide the sum by the number of neighborhoods to get average
			tempParams[i] /= tempLen[i]
			tempParams[i] = int(tempParams[i])
			# check if we need to keep moving by seeing if the percent change is less than threshold
			if (abs(tempParams[i]-self.params[i])/self.params[i] > self.movePercent):
				self.needsToMove = True
		# set the center (params) based on the new calculated params
		self.params = tempParams[:]

## Function to calculate the distance between a neighborhood and a state
## based on the normalized euclidean distance
def calculateDistance(neighborhood, state, paramNames, paramsMax, paramsMin):
	distance = 0
	for index, paramName in enumerate(paramNames):
		if paramName in neighborhood:
			if neighborhood[paramName] is not None: # for null parameters
				# calculate (xn-yn)^2
				sub = int(neighborhood[paramName])-state.params[index]
				# normalize by axis range
				normalize = sub/(paramsMax[index]-paramsMin[index])
				square = normalize**2
				distance += square
	# sum tpgether distances for each parameter
	distance = math.sqrt(distance)
	return distance

## Function to find the closes centroid to a given neighborhood
## uses the euclidean distance formula
def findClosestCentroid(neighborhood, centroids, paramNames, paramsMax, paramsMin):
	min_distance = float("inf")
	closestState = centroids[0]
	# Find which of the states has the shortest distance to this neighborhood
	for state in centroids:
		if calculateDistance(neighborhood, state, paramNames, paramsMax, paramsMin) < min_distance:
			min_distance = calculateDistance(neighborhood, state, paramNames, paramsMax, paramsMin)
			closestState = state
	return closestState

def kmeans(data, k=None):
	if k is None:
		cfg = SafeConfigParser()
		cfg.read('config.cfg')
		k = cfg.getint('modeling', 'num_states')

	props = {
		'Housing Units': [],
		'Impoverished Pop': [],
		'Median Contract Rent': [],
		'Median Home Value': [],
		'Median Household Income': [],
	}

	# Find minimum and maximum values for all properties
	for prop in props.keys():
		for neighborhood_datum in data:
			if prop in neighborhood_datum:
				if neighborhood_datum[prop] is not None:
					props[prop].append(int(neighborhood_datum[prop]))

	prop_mins = [min(prop) for prop in props.values()]
	prop_maxs = [max(prop) for prop in props.values()]

	# start centroids based on the first points
	point_list = []
	i = 0
	params1 = [0]*len(props)
	while len(point_list) < k:
		append = True
		params = params1[:] # we need copies of the object
		# copy all of the parameters into a list
		for prop_index, prop in enumerate(props.keys()):
			if prop in data[i]:
				if data[i][prop] is not None:
					params[prop_index] = int(data[i][prop])
				else:
					# if even one of the parameters is null, we don't want to use this point
					append = False
		if append:
			point_list.append(params)
		i+=1

	# Create states based on the centroids
	states = []
	for point in point_list:
		states.append(State(point))

	# loop until centroids stop moving
	needsToMove = True
	while (needsToMove):
		needsToMove = False
		# clear all neighborhoods from centroids
		for c in states:
			c.neighborhoods = []

		# assign neighborhoods
		for neighborhood in data:
			state = findClosestCentroid(neighborhood, states, props.keys(), prop_maxs, prop_mins)
			state.neighborhoods.append(neighborhood)

		## Move the centroids
		for c in states:
			c.getNewCenter(props.keys())
			# if any need to move, then set needsToMove to true
			needsToMove = needsToMove or c.needsToMove

		# Uncomment this if you want to print the num neighborhoods in each state	
		# 	print str(len(c.neighborhoods)) + ", ",
		# print

if __name__ == "__main__":
	with open('data/data.json') as data_file:
		data = json.load(data_file)
	kmeans(data)