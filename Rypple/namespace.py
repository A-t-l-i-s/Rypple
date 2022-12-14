__all__=["Rypple_Namespace"]





class Rypple_Namespace(object):
	def __new__(cls,values={}):
		self = object.__new__(cls)

		object.__setattr__(self,"__values__",values)

		return self





	def __getattr__(self,attr):
		d = self.__dict__
		v = d["__values__"]

		return v.get(attr)



	def __setattr__(self,attr,val):
		d = self.__dict__["__values__"]
		d[attr] = val





	def __getitem__(self,attr):
		return self.__getattr__(attr)



	def __setitem__(self,attr,value):
		self.__setattr__(attr,value)





	def values(self):
		return self.__dict__["__values__"]




	def contains(self,var):
		return (var in self.__dict__["__values__"])




	def pop(self,attr):
		v= self.__dict__["__values__"]

		if (attr in v):
			return v.pop(attr)





	def toJSON(self):
		out = {}

		for k,v in self.values().items():
			if (isinstance(v,type(self))):
				out[k] = v.toJSON()

			else:
				out[k] = v

		return out





