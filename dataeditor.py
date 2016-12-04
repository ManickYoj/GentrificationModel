import json
import os
import geojson
from census import Census
from us import states


# -- Config
COUNTIES = {
	"Suffolk": "025",		# Boston
	"Middlesex": "017",	# Somerville/Cambridge
	"Essex": "009" 			# The stuff in the north
}

VARIABLES = {
	'Tract Name': 'NAME',
	'Population': 'B01003_001E',
	'Median Household Income': 'B19013_001E',
	'Median Contract Rent': 'B25058_001E',
	'Median Home Value': 'B25077_001E',
	# 'Employed': 'B23025_004E',
	# 'Unemployed': 'B23025_005E',
	# 'Commute Time (minutes)': 'B08136_001E', # Not included in the 2010 ACS5 data
	'Impoverished Pop': 'B17001_002E',
}

GEOJSON_VARS = {
	'Housing Units': 'HU100_RE',
}

ALIASES = {value: key for key, value in VARIABLES.items()}

# -- Definitions

def loadAPIKey(name):
	with open("./private.json", 'r') as private:
		apiKey = json.load(private)['API-keys'][name]
	return apiKey

class Data:
	def __init__(self, load=False, filepath="data.json"):
		self.filepath = filepath
		if load and os.path.isfile(filepath):
			with open(filepath, "r") as datafile:
				self.data = json.load(datafile)
		else:
			self.data = {}

	def alias(self, datum, aliases=ALIASES):
		'''
		Given a dictionary with census encoded keys
		(eg. B01003_001E), replaces those keys with
		a human readable key (eg. 'Population') based
		on the `aliases` argument. The `aliases` argument
		should be a dictionary of `census code: alias`
		key/value pairs.
		'''
		aliasedDatum = {}

		for key, value in datum.items():
			if key in ALIASES:
				aliasedDatum[aliases[key]] = value
			else:
				aliasedDatum[key] = value

		return aliasedDatum

	def update(self, tractID, newdata, addNew=False):
		'''
		Add the keys and values from `newdata` to the
		data object, aliasing the key names.

		Strictly updates (does not add a new item to the
		data object) unless the `addNew` parameter is
		set to `True`.
		'''
		aliasedData = self.alias(newdata)
		if tractID in self.data:
			for key, value in aliasedData.items():
				self.data[tractID][key] = str(value)

		elif addNew:
			self.data[tractID] = aliasedData

	def save(self):
		'''
		Saves the data to the data file.
		'''
		listdata = self.data.values()

		with open(self.filepath, "w") as datafile:
			json.dump(
				listdata,
				datafile,
				sort_keys=True,
				indent=2,
				separators=(',', ": ")
			)


# -- Running Code

if __name__ == "__main__":
	c = Census(loadAPIKey('census'));
	data = Data()

	# Pull census data to create the data file
	for county in COUNTIES.keys():
		tractdata = c.acs5.state_county_tract(
			VARIABLES.values(),
			states.MA.fips,
			COUNTIES[county],
			Census.ALL,
			year="2010"
		)

		for tractdatum in tractdata:
			data.update(tractdatum['tract'], tractdatum, True)

	# Augment with data loaded from downloaded geojson
	with open('geodata.geojson', 'r') as geodata:
		geofeatures = geojson.load(geodata)['features']

	for tract in geofeatures:
		tractID = tract['properties']['TRACTCE10']
		longitude, latitude = tract['geometry']['coordinates']
		data.update(tractID, {
			'Latitude': latitude,
			'Longitude': longitude
		})

		for propname, prop in GEOJSON_VARS.items():
			data.update(tractID, {
				propname: tract['properties'][prop]
			})

	data.save()