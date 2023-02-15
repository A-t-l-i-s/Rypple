from .namespace import *





__all__=["Rypple_Extension","Rypple_ExtensionKey"]





class Rypple_ExtensionKey(object):
	name:str = None
	description:str = None

	parameters:str = None

	enabled:bool = False



	def callback(cls,step,scope,namespace):
		...








class Rypple_Extension(object):
	name:str = None
	description:str = None
	
	enabled:bool = False



	def init(cls,scope):
		...



	@classmethod
	def list(cls):
		for d in dir(cls):
			v = getattr(cls,d)

			if (isinstance(v,type) and issubclass(v,Rypple_ExtensionKey)):
				yield v



	@classmethod
	def get(cls,key):
		for k in cls.list():
			if (k.name == key):
				return k
		




