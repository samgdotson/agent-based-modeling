# Infection class

class infection(object):
	"""This is the class implementation for a model infection"""
	def __init__(self, mortality):
		super(infection, self).__init__()
		self.mortality = mortality
