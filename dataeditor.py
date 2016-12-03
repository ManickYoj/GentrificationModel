import json
import os
from census import Census
from us import states
# import requests
# from requests.auth import HTTPBasicAuth


# -- Config
COUNTIES = {
	"suffolk": "025",		# Boston
	"middlesex": "017",	# Somerville/Cambridge
	"essex": "009" 			# The stuff in the north
}

# -- Definitions

def loadAPIKey(name):
	with open("./private.json", 'r') as private:
		apiKey = json.load(private)['API-keys'][name]
	return apiKey

class Data:
	def __init__(self, filepath="data.json"):
		self.filepath = filepath
		if os.path.isfile(filepath):
			with open(filepath, "r") as datafile:
				self.data = json.load(datafile)
		else:
			self.data = {}

	def addNoSave(self, name, datum):
		self.data[name] = datum

	def add(self, name, datum):
		self.addNoSave(name, datum)
		self.save()

	def save(self):
		with open(self.filepath, "w") as datafile:
			json.dump(
				self.data,
				datafile,
				sort_keys=True,
				indent=2,
				separators=(',', ": ")
			)


# -- Running Code

if __name__ == "__main__":
	c = Census(loadAPIKey('census'));
	data = Data()

	for county in COUNTIES.keys():
		data.add(
			county,
			c.sf1.state_county_tract(
			'NAME',
			states.MA.fips,
			COUNTIES[county],
			Census.ALL
		))
