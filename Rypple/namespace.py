from .step import *





__all__=["Rypple_Namespace"]





class Rypple_Namespace(object):
	def __new__(cls,values={},temp=False):
		self = object.__new__(cls)

		object.__setattr__(self,"__temp__",temp)
		object.__setattr__(self,"__values__",dict(values))

		return self





	# ~~~~~~~~ Attr Assignment ~~~~~~~
	def __getattr__(self,attr):
		d = self.__dict__
		v = d["__values__"]

		return v.get(attr)





	def __setattr__(self,attr,val):
		d = self.__dict__["__values__"]
		d[attr] = val
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ Item Assignment ~~~~~~~
	def __getitem__(self,attr):
		p = attr.split(".")

		if (len(p) > 1):
			attr = p.pop(-1)
			s = self.parent(p)

			if (s != None):
				return Rypple_Namespace.__getattr__(s,attr)

		else:
			return self.__getattr__(attr)





	def __setitem__(self,attr,value):
		p = attr.split(".")

		if (len(p) > 1):
			attr = p.pop(-1)
			s = self.parent(p)

			if (s != None):
				return Rypple_Namespace.__setattr__(s,attr,value)

		else:
			self.__setattr__(attr,value)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Functions ~~~~~~~~~~
	def values(self):
		return self.__dict__["__values__"]





	def keys(self):
		return tuple(
			self.__dict__["__values__"].keys()
		)
		





	def contains(self,attr):
		p = attr.split(".")

		if (len(p) > 1):
			attr = p.pop(-1)
			s = self.parent(p)

			if (s != None):
				return s.contains(attr)

		else:
			return (attr in self.__dict__["__values__"])





	def parent(self,path):
		s = self
		
		for i,a in enumerate(path):
			v = s[a]

			if (isinstance(v,Rypple_Namespace)):
				s = v

			else:
				s = None
				break


		return s





	def pop(self,attr):
		v= self.__dict__["__values__"]

		if (attr in v):
			return v.pop(attr)




	def removeTemps(self):
		def call(ns):
			for k in ns.keys():
				v = ns[k]

				if (isinstance(v,Rypple_Namespace)):
					if (v.__temp__):
						ns.pop(k)

					else:
						call(v)


				elif (isinstance(v,Rypple_Step)):
					if (v.temp):
						ns.pop(k)




		call(self)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ JSON Conversion ~~~~~~~
	def toJSON(self):
		out = {}

		for k,v in self.values().items():
			if (isinstance(v,(type(self),Rypple_Step))):
				out[k] = v.toJSON()

			else:
				out[k] = v

		return out
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





