import json
from ConfigParser import SafeConfigParser

#This function will add a list of states for every tract
#to the geojson file containing their location and other data
#It takes in a dictionary of the form {tractNumber:[list of states over time]}
def configureGeojson(modelData):
	#Load all variable from config file
	cfg = SafeConfigParser()
	cfg.read("config.cfg")
	num_states = cfg.getint("modeling", "num_states")
	year_max = cfg.getint("modeling", "year_max")
	year_min = cfg.getint("modeling", "year_min")

	#Load geodata file representing where each tract is
	with open('data/geodata.geojson') as data_file:
			basegeojson = json.load(data_file)

	#Initalize a new json as to not write over any original data
	geojson = {
		"features": [],
	}

	#Loop through all elements of the given geodata
	for obj in basegeojson["features"]:
		#Find the tract number for each element
		tract = obj["properties"]["TRACTCE10"]
		#Find the matching tract number in the modelData taken from the Markov model
		if tract in modelData:
			#set the states attribute of that tract object to
			#the list of states from the model data
			obj["properties"]["states"] = modelData[tract]
			geojson["features"].append(obj)

	#Sets the variables from the config file to part of the geojson data
	#so that these vairables can be used in calculations on the front-end
	geojson["numStates"] = num_states
	geojson["minYear"] = year_min
	geojson["maxYear"] = year_max

	#Write the geojson data into a new file
	#so that the origina data doesn't get overwritten
	with open('data/gent-geodata.geojson', 'w') as outfile:
	    json.dump(geojson, outfile)
