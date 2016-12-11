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


class KMeans:
	def __init__(self, data, num_states=None):
		# Set number of states (k) based on the config file
		if num_states == None:
			cfg = SafeConfigParser()
			cfg.read("config.cfg")
			self.num_states = cfg.getint("modeling", "num_states")
		else:
			self.num_states = num_states

		# Names of the parameters in data
		self.paramNames = []

		# lists of the max and min params
		self.paramsMax = []
		self.paramsMin = []

		# data (json)
		self.data = data

		self.states = []
		self.kmeans()

	def calcMinMaxParams(self):

		props = {
		'Housing Units': [],
		'Impoverished Pop': [],
		'Median Contract Rent': [],
		'Median Home Value': [],
		'Median Household Income': [],
		}

		# Find minimum and maximum values for all properties
		for prop in props.keys():
			for neighborhood_datum in self.data:
				if prop in neighborhood_datum:
					if neighborhood_datum[prop] is not None:
						props[prop].append(int(neighborhood_datum[prop]))

		self.paramsMin = [min(prop) for prop in props.values()]
		self.paramsMax = [max(prop) for prop in props.values()]
		self.paramNames = props.keys()


	## Function to calculate the distance between a neighborhood and a state
	## based on the normalized euclidean distance
	def calculateDistance(self, neighborhood, state):
		distance = 0
		for index, paramName in enumerate(self.paramNames):
			if paramName in neighborhood:
				if neighborhood[paramName] is not None: # for null parameters
					# calculate (xn-yn)^2
					sub = int(neighborhood[paramName])-state.params[index]
					# normalize by axis range
					normalize = sub/(self.paramsMax[index]-self.paramsMin[index])
					square = normalize**2
					distance += square
		# sum tpgether distances for each parameter
		distance = math.sqrt(distance)
		return distance


	## Function to find the closes centroid to a given neighborhood
	## uses the euclidean distance formula
	def findClosestCentroid(self, neighborhood):
		min_distance = float("inf")
		closestState = self.states[0]
		# Find which of the states has the shortest distance to this neighborhood
		for state in self.states:
			if self.calculateDistance(neighborhood, state) < min_distance:
				min_distance = self.calculateDistance(neighborhood, state)
				closestState = state
		return closestState

	def createInitialStates(self):
		# start centroids based on the first points
		point_list = []
		i = 0
		params1 = [0]*len(self.paramNames)
		while len(point_list) < self.num_states:
			append = True
			params = params1[:] # we need copies of the object
			# copy all of the parameters into a list
			for j in range(len(self.paramNames)):
				if self.paramNames[j] in self.data[i]:
					if self.data[i][self.paramNames[j]] is not None:
						params[j] = int(self.data[i][self.paramNames[j]])
					else:
						# if even one of the parameters is null, we don't want to use this point
						append = False
			if append:
				point_list.append(params)
			i+=1

		# Create states based on the centroids
		for point in point_list:
			self.states.append(State(point))

	def kmeans(self):
		self.calcMinMaxParams()
		self.createInitialStates()

		# loop until centroids stop moving
		needsToMove = True
		while (needsToMove):
			needsToMove = False
			# clear all neighborhoods from centroids
			for c in self.states:
				c.neighborhoods = []

			# assign neighborhoods
			for neighborhood in self.data:
				state = self.findClosestCentroid(neighborhood)
				state.neighborhoods.append(neighborhood)

			## Move the centroids
			for c in self.states:
				c.getNewCenter(self.paramNames)
				# if any need to move, then set needsToMove to true
				needsToMove = needsToMove or c.needsToMove

			# Uncomment this if you want to print the num neighborhoods in each state
			# 	print str(len(c.neighborhoods)) + ", ",
			# print

	def classifyNeighborhoods(self, data):
		# classify by returning a dictionary of tract:state pairs
		# tracts are described by a number, but stored as a string type
		neighborhoods = []

		for neighborhood in data:
			neighborhoodDict = {}
			state = self.findClosestCentroid(neighborhood)
			stateIndex = self.states.index(state)
			neighborhoodDict['tract'] = neighborhood['tract']
			neighborhoodDict['states'] = [stateIndex]
			neighborhoods.append(neighborhoodDict)

		return neighborhoods


if __name__ == "__main__":
	with open('data/2010.json') as data_file:
		data = json.load(data_file)
	k = KMeans(data)
	print k.classifyNeighborhoods(data)