from configparser import ConfigParser


class Config(object):
	# def __new__(cls,*args,**kwargv):
	# 	if not hasattr(cls,'_instance'):
	# 		cls._instance = super(Config,cls).__new__(cls,*args,**kwargv)
	# 	return cls._instance

	def __init__(self,path):
		self.path = path


	def get_config_value(self,section,key):
		config = ConfigParser()
		try:
			config.read(self.path,encoding='UTF-8')
			return config.get(section,key)
		except Exception,e:
			raise Exception(e.message)


	def get_section_options_value(self,section):
		config = ConfigParser()
		try:
			config.read(self.path,encoding='UTF-8')
			options = config.options(section)
			values = []
			for o in options:
				values.append(config.get(section,o))
			option_values = zip(options,values)
			return dict((k,v) for k,v in option_values)
		except Exception,e:
			raise Exception(e.message)