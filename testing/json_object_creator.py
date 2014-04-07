import json


class Path_creator:
	def __init__(self, name, dst):
		self.dst = dst
		self.name = name
		dic = self.__dict__()

		open_string = 'objects\\%s.json' % (self.name)

		with open(open_string, 'w') as outfile:
			json.dump(dic, outfile, indent=4, sort_keys=True)

	def __dict__(self):
		return dict({self.name:self.dst})

	def add_path(self):
		dic = self.__dict__()

		open_string = 'objects\\%s.json' % (self.name)

		with open(open_string, 'w') as outfile:
			json.dump(dic, outfile, indent=4, sort_keys=True)

Dropbox = Path_creator('Dropbox','D:\\Temp')
print(Dropbox.__dict__())
#Dropbox.add_path()

JSONopen = open('temp.json')
JSONdata = json.load(JSONopen)

print(JSONdata['Dropbox'])
