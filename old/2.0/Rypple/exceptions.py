import copy





__all__=["Rypple_Exception","Unknown"]





class Rypple_Exception(object):
	text:str = None


	def __new__(cls,text=None):
		self = copy.copy(cls)

		self.text = text

		return self







class Unknown(Rypple_Exception):
	...








