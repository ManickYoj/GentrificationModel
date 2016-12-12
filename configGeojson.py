import json
from ConfigParser import SafeConfigParser

def configureGeojson(modelData):
	cfg = SafeConfigParser()
	cfg.read("config.cfg")
	num_states = cfg.getint("modeling", "num_states")
	year_max = cfg.getint("modeling", "year_max")
	year_min = cfg.getint("modeling", "year_min")

	#load geodata file representing where each tract is
	with open('data/geodata.geojson') as data_file:
			geojson = json.load(data_file)

	#load data from model indicating which states each tract is in

	#loop through all elements of the geodata
	for obj in geojson["features"]:
		#find the tract number for each element
		tract = int(obj["properties"]["TRACTCE10"])
		if tract in modelData:
			#set the states attribute of that tract object to 
			#the list of states from the model data
			obj["properties"]["states"] = modelData[tract]

	print (year_max-year_min)
	geojson["numStates"] = num_states
	geojson["minYear"] = year_min
	geojson["maxYear"] = year_max

	#write the geojson data into a new file
	#so that the origina data doesn't get overwritten
	with open('data/gent-geodata.geojson', 'w') as outfile:
	    json.dump(geojson, outfile)
