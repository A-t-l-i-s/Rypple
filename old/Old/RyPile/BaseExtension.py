from typing import *





__all__=["BaseExtension","BaseExtensionKey"]





class BaseExtensionKey:
	enabled=False

	name=None


	def callback(extension,parent,scope,step):
		...







class BaseExtension:
	enabled=False

	name=None

	executable=None
	extensions=()



	def execute(extension,parent,scope):
		...



	@classmethod
	def list(cls):
		keys=[]

		for k in dir(cls):
			attr=getattr(cls,k)

			if (type(attr) == type):
				if (issubclass(attr,BaseExtensionKey)):
					keys.append(attr)


		return keys




	@classmethod
	def get(cls,key):
		for k in cls.list():
			if (k.name == key):
				return k


		return None




