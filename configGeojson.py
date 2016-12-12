import json
from ConfigParser import SafeConfigParser

cfg = SafeConfigParser()
cfg.read("config.cfg")
num_states = cfg.getint("modeling", "num_states")
year_max = cfg.getint("modeling", "year_max")
year_min = cfg.getint("modeling", "year_min")

#load geodata file representing where each tract is
with open('data/geodata.geojson') as data_file:
		geojson = json.load(data_file)

#load data from model indicating which states each tract is in
modelData = {418003:[1, 2, 3, 4, 5],
417701:[2, 3, 4, 5, 6],
417702:[3, 4, 5, 6, 7],
418102:[4, 5, 6, 7, 8],
418004:[5, 6, 7, 8, 9],
412300:[6, 7, 8, 9, 1],
412200:[7, 8, 9, 1, 2],
404400:[8, 9, 1, 2, 3]}

#loop through all elements of the geodata
for obj in geojson["features"]:
	#find the tract number for each element
	tract = int(obj["properties"]["TRACTCE10"])
	if tract in modelData:
		#set the states attribute of that tract object to 
		#the list of states from the model data
		obj["properties"]["states"] = modelData[tract]

print (year_max-year_min)
geojson["num_states"] = num_states
geojson["num_years"] = year_max-year_min

#write the geojson data into a new file
#so that the origina data doesn't get overwritten
with open('data/gent-geodata.geojson', 'w') as outfile:
    json.dump(geojson, outfile)
