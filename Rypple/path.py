import json
import ntpath
from dataclasses import dataclass, field





__all__=["Rypple_Path"]





@dataclass(kw_only=True)
class Rypple_Path(object):
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	base:int = -1
	path:list = field(default_factory=list)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~ List Manipulation ~~~~~~
	def pop(self,i):
		if (len(self.path) > 0):
			self.path.pop(i)




	def add(self,id):
		self.path.append(id)




	def found(self,id):
		if (len(self.path) > 0):
			if (self.path[-1] == id):
				return True


		return False



	@property
	def first(self):
		if (len(self.path) > 0):
			return self.path[0]



	@property
	def last(self):
		if (len(self.path) > 0):
			return self.path[-1]
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



