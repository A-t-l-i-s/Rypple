import json

from .step import *





__all__ = ("Rypple_Namespace",)





class Rypple_Namespace:
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	defaults = {
		"__temp__": Rypple_Step.temp,
	}
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	def __init__(self,value={}):


		# If is new namespace
		if (isinstance(value,Rypple_Namespace)):
			values = value.values()

		# If is dict
		elif (isinstance(value,dict)):
			values = value

		# Else raise value error
		else:
			raise ValueError()


		# Default values
		for k,v in self.defaults.items():
			if (k not in values):
				values[k] = v


		# Set values attribute
		object.__setattr__(self,"__values__",values)






	def __len__(self):
		return len(self.values().keys())





	# ~~~~~~~~ Attr Assignment ~~~~~~~
	def __getattr__(self,attr):
		v = self.values()

		return v.get(attr)





	def __setattr__(self,attr,val):
		v = self.values()
		
		v[attr] = val
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ Item Assignment ~~~~~~~
	def __getitem__(self,attr):
		# Get path
		path = attr.split(".")

		if (len(path) > 1):
			# Get final attribute
			attr = path[-1]

			# Get parent
			parent = self.parent(path)

			if (parent != None):
				return Rypple_Namespace.__getattr__(parent,attr)


		else:
			return self.__getattr__(attr)





	def __setitem__(self,attr,value):
		# Get path
		path = attr.split(".")

		if (len(path) > 1):
			# Get final attribute
			attr = path[-1]

			# Get parent
			parent = self.parent(path)

			if (parent != None):
				return Rypple_Namespace.__setattr__(parent,attr,value)


		else:
			self.__setattr__(attr,value)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Functions ~~~~~~~~~~
	def values(self):
		d = self.__dict__
		v = d["__values__"]

		return v





	def keys(self):
		return tuple(self.values().keys())





	def items(self):
		return self.values().items()
		





	def contains(self,attr):
		# Get path
		path = attr.split(".")

		if (len(path) > 1):
			# Get final attribute
			attr = path[-1]

			# Get parent
			parent = self.parent(path)

			if (parent != None):
				return parent.contains(attr)

		else:
			return (attr in self.values())





	def parent(self,path):
		# Default parent
		parent = None


		if (len(path) > 0):
			# Set parent
			parent = self
			
			for i,a in enumerate(path[:-1]):
				# Get value in namespace
				val = parent[a]

				if (isinstance(val,Rypple_Namespace)):
					# Set new parent
					parent = val

				else:
					# Doesn't exist or invalid value
					parent = None
					break


		return parent





	def pop(self,attr):
		# Get path
		path = attr.split(".")

		if (len(path) > 1):
			# Get final attribute
			attr = path[-1]

			# Get parent
			parent = self.parent(path)

			parent.pop(attr)

		else:
			self.values().pop(attr)




	def verify(self,data):
		for k,v in data.items():
			if (isinstance(v,dict)):
				v = Rypple_Namespace(v)

			if (not self.contains(k)):
				self[k] = v





	def resolve(self):
		def removeTemps(values):
			# Iterate through values
			if (isinstance(values,dict)):
				keys = tuple(values.keys())
			else:
				keys = range(len(values))


			for k in keys:
				v = values[k]

				# If namespace
				if (isinstance(v,Rypple_Namespace)):
					if (v.__temp__):
						# Remove namespace
						values.pop(k)

					else:
						# Iterate through next namespace
						removeTemps(v.values())


				elif (isinstance(v,Rypple_Step)):
					if (v.temp):
						# Remove step
						values.pop(k)

					else:
						# Iterate through next steps
						removeTemps(v.children)



		# Remove all temps
		removeTemps(self.values())
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ JSON Conversion ~~~~~~~
	def toJSON(self):
		out = {}

		for k,v in self.items():
			if (k not in self.defaults):
				if (isinstance(v,(Rypple_Namespace,Rypple_Step))):
					out[k] = v.toJSON()

				else:
					out[k] = v

		return out





	def toSteps(self):
		base = Rypple_Step(
			key = "Base"
		)


		for k,v in self.items():
			if (k not in self.defaults):
				step = Rypple_Step(
					key = k,
					value = v
				)


				if (isinstance(v,Rypple_Namespace)):
					step.value = None

					base_ = v.toSteps()
					step.children = base_.children


				elif (isinstance(v,Rypple_Step)):
					step.key = "Function"
					step.value = k

					step.children = v.children


				base.children.append(step)


		return base
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~~ Print ~~~~~~~~~~~~
	def print(self):
		# Convert to JSON
		jsonData = self.toJSON()

		# Dump data to string
		data = json.dumps(jsonData,indent=4)

		# Print data
		print(data)






	def printList(self):
		def call(parent,namespace):

			# Default signs
			signs = ""

			# Temp sign
			if (namespace.__temp__):
				signs += "~"


			for k,v in namespace.items():
				# If not a hidden default value
				if (k not in Rypple_Namespace.defaults):
					# Format path
					path = f"{parent}.{k}".strip(".")

					# Get path indentation
					c = path.count(".")


					# If value is another namespace
					if (isinstance(v,Rypple_Namespace)):
						print(("\t" * c) + signs + path + ":")

						# Iterate through new namespace
						call(path,v)

					else:
						print(("\t" * c) + signs + path + f": {v}")



		# Initialize iteration
		call("",self)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


