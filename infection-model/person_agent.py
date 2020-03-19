# This class describes a person agent

class person(object):
	"""An individual person"""
	def __init__(self, age, healthy, max_range,):
		super(person, self).__init__()
		self.age = age
		self.healthy = healthy
		self.max_range = max_range
		