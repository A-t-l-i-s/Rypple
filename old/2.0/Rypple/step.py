import json
import zlib
import ntpath
from dataclasses import dataclass, field

from .path import *





__all__=["Rypple_Step"]





@dataclass(kw_only=True)
class Rypple_Step(object):
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	key:str = None
	value:str = None
	level:int = -1
	id:int = -1
	parent:str = -1
	temp:bool = False

	steps:list = field(default_factory=list)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ JSON Conversion ~~~~~~~
	def toJSON(self):
		return {
			"key":			self.key,
			"value":		self.value,
			"level":		self.level,
			"id":			self.id,
			"parent":		self.parent,
			"temp":			self.temp,

			"steps":		[s.toJSON() for s in self.steps],
		}





	@classmethod
	def fromJSON(cls,data):
		self=object.__new__(cls)


		self.key=			data.get("key",None)
		self.value=			data.get("value",None)
		self.level=			data.get("level",-1)
		self.id=			data.get("id",-1)
		self.parent=		data.get("parent",-1)
		self.temp=			data.get("temp",False)

		self.steps=			[cls.fromJSON(s) for s in data.get("steps",[])]


		return self
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~ Bytecode Conversion ~~~~~
	def toBytecode(self):
		arr = self.toJSON()

		buf = json.dumps(arr)
		buf = buf.encode()


		try:
			comp = zlib.compress(buf)
		except:
			comp = None


		return comp





	@classmethod
	def fromBytecode(cls,data):
		try:
			buf = zlib.decompress(data)

			arr = json.loads(buf)

			groups = cls.fromJSON(arr)
		except:
			groups = None


		return groups
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Functions ~~~~~~~~~~
	def compare(self,keys):
		for k,v in keys.items():
			if (self[k] != v):
				return False

		return True





	def getPath(self,**keys):
		def iterate(step):
			for s in step.steps:
				path.add(s.id)

				if (s.compare(keys)):
					return True

				else:
					if (iterate(s)):
						return True

					else:
						path.pop(-1)


			return False

				


		path = Rypple_Path(base=self.id)
		iterate(self)

		return path





	def getIndex(self,**keys):
		for i,s in enumerate(self.steps):
			if (s.compare(keys)):
				return i


		return -1






	def find(self,**keys):
		def iterate(step):
			for s in step.steps:
				if (s.compare(keys)):
					yield s

				for s_ in iterate(s):
					yield s_

				

		return iterate(self)






	def get(self,path):
		def iterate(step):
			for s in step.steps:
				f = path.first

				if (f != None):
					if (f == s.id):
						if (s.id == path.last):
							return s

						else:
							path.pop(0)
							return iterate(s)

				else:
					return step



		if (path.base == self.id):
			return iterate(self)



		return None





	def isCmd(self):
		if (self.value != None):
			return True

		else:
			return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~ Magic Methods ~~~~~~~~
	def __iter__(self):
		return self.steps.__iter__()



	def __getitem__(self,key):
		if (hasattr(self,key)):
			return getattr(self,key)



	def __setitem__(self,key,value):
		if (hasattr(self,key)):
			setattr(self,key,value)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




