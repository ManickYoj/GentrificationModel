import random
from ConfigParser import SafeConfigParser

class Markov:
	def __init__(self, neighborhoodDict, probMatrix, yearMin=None, yearMax=None):
		# read from config file
		if yearMin == None:
			cfg = SafeConfigParser()
			cfg.read("config.cfg")
			yearMin = cfg.getint("modeling", "year_min")
		if yearMax == None:
			cfg = SafeConfigParser()
			cfg.read("config.cfg")
			yearMax = cfg.getint("modeling", "year_max")

		self.neighborhoods = neighborhoodDict
		self.probMatrix = probMatrix
		self.numYears = yearMax - yearMin
		self.simulatedStates = {}
		self.initSimulatedDict()
	
	# Create new dictionary with tracts, but just the first year based on data
	def initSimulatedDict(self):
		for tract in self.neighborhoods:
			self.simulatedStates[tract] = [self.neighborhoods[tract][0]]

	# calculate the rest of the data based off the first year
	def runSim(self):
		for tract in self.simulatedStates:
			for year in range(self.numYears): # start after the first year
				# print self.simulatedStates[tract]
				currentState = self.simulatedStates[tract][year]
				# select the next state based on probabilities
				randSumGoal = random.random() # so that [0.0,1.0)
				sumProbs = 0
				nextState = -1
				# add to sum until it reaches rand number, then save that state
				while sumProbs < randSumGoal:
					nextState += 1										
					sumProbs += self.probMatrix[currentState][nextState]
				# add chosen state to the end of the list
				self.simulatedStates[tract].append(nextState)
		return self.simulatedStates

		