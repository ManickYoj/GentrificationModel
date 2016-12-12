import kmeans
import trainer
import json
# Import all data



if __name__ == "__main__":
	datafilenames = ['data/2010.json', 'data/2011.json', 'data/2012.json', 'data/2013.json']
	datafiles = []
	for filename in datafilenames:
		with open(filename) as data_file:
			data = json.load(data_file)
			datafiles.append(data)
	k = kmeans.KMeans(datafiles[0]) # train on first year
	neighborhoodDict = k.classifyNeighborhoods(datafiles)
	# form is {'tract':<tract>, 'states':[<list of states over time>]}

	# Bayesian
	# input: {'tract':<tract>, 'states':[<list of states over time>]}
	# outputs: kxk matrix
	#		[[from state 1 to all others], ...]
	probMatrix, testData = trainer.trainModel(neighborhoodDict)
	trainer.visualize(probMatrix)

	# Model stuff
	# input: neighborhoodDict, probMatrix
	# output: json {'tract':<tract>, 'states':[<list of states over time>]}
	# this will fill in the list
	# m = Markov(neighborhoodDict, probMatrix)
	# outputDict = m.run()

	# Export for viz
	# want json {'tract':<tract>, 'states':[<list of states over time>]}
