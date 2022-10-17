import json
from os.path import exists

def load():
	global data
	file_exists = exists("dict.json")
	if file_exists:
		file = open("dict.json", "r")
		data = json.loads(file.read())
	else:
		data = []
		print("dict.json not found, creating a new one")
		open("dict.json", "w").close()

def save():
	file = open("dict.json", "w")
	file.write(json.dumps(data, indent=4))

def add(plant):
	data.append(plant)
	save()

def remove(plant):
	data.remove(plant)
	save()