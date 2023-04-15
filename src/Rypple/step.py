import sys
import uuid
import zlib
import orjson

from dataclasses import dataclass, field





__all__ = ("Rypple_Step",)





@dataclass(kw_only = True)
class Rypple_Step:
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	key:str = None
	value:str = None
	id:str = -1
	level:int = -1

	temp:bool = False
	thread:bool = False

	children:list = field(default_factory=list)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~ Class Methods ~~~~~~~~
	@classmethod
	def newId(cls):
		uid = uuid.uuid1()
		id_ = uid.hex.lower()

		return id_
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Methods ~~~~~~~~~~~
	def hasValue(self):
		return self.value != None
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Children ~~~~~~~~~~~
	def addChild(self,child):
		if (isinstance(child,Rypple_Step)):
			self.children.append(child)





	def hasChildren(self):
		if (len(self.children) > 0):
			return True

		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ JSON Conversion ~~~~~~~
	def toJSON(self):
		out = {
			"key":			self.key,
			"value":		self.value,
			"level":		self.level,

			"temp":			self.temp,
			"thread":		self.thread,

			"children":		[]
		}

		# Convert children to json
		for s in self.children:
			out["children"].append(
				s.toJSON()
			)


		return out





	@classmethod
	def fromJSON(cls,data):
		self=object.__new__(cls)


		self.key=			data.get("key",		cls.key)
		self.value=			data.get("value",	cls.value)
		self.id=			cls.newId()
		self.level=			data.get("level",	cls.level)

		self.temp=			data.get("temp",	cls.temp)
		self.thread=		data.get("thread",	cls.thread)

		self.children=		[]

		# Load children from json
		for s in data.get("children",[]):
			self.children.append(
				cls.fromJSON(s)
			)


		return self
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	


	# ~~~~~~~~ Byte Conversion ~~~~~~~
	def toBytecode(self):
		# Get as JSON
		jsonData = self.toJSON()

		# Convert to bytes
		data = orjson.dumps(jsonData)

		# Deflate data
		out = zlib.compress(data)

		return out





	@classmethod
	def fromBytecode(cls,data):
		if (isinstance(data,(bytes,bytearray))):
			try:
				# Attempt to inflate data
				newData = zlib.decompress(data)

				# Load data as json
				jsonData = orjson.loads(newData)
				
				# Create new step and return it
				return cls.fromJSON(jsonData)

			except:
				...


		return None





	def toFile(self,path):
		# To bytes
		data = self.toBytecode()

		# Open file
		with open(path,"wb") as file:
			# Write to file
			file.write(data)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~~ Print ~~~~~~~~~~~~
	def print(self):
		jsonData = self.toJSON()

		out = orjson.dumps(jsonData,option=orjson.OPT_INDENT_2)
		out = out.decode("utf-8")

		sys.stdout.write(out + "\n")





	def printList(self):
		def call(parent,children):
			# Iterate through children
			for v in children:
				# Get values
				key = v.key
				val = v.value

				# Format path
				path = f"{parent}.{key}".strip(".")
				
				# Get inent count
				c = path.count(".")


				# If value is nothing
				if (val == None):
					val = ""


				# Default signs
				signs = ""

				# Temp sign
				if (v.temp):
					signs += "~"

				# Run sign
				if (v.thread):
					signs += "*"


				if (val):
					valOut = f": {val}"
				else:
					valOut = ""


				# Print step
				sys.stdout.write(("\t" * c) + signs + path + valOut + "\n")


				# Iterate through next step
				call(path,v.children)



		# Initialize iteration
		call("",self.children)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~







