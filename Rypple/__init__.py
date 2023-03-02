import re
import glob
from pathlib import Path

from .step import *
from .scope import *
from .namespace import *
from .extension import *





__all__ = ("Rypple",)





class Rypple:
	# Code delimiter
	delimiter: str = ":"
	comment: str = "#"

	tempSign: str = "~"
	threadSign: str = "*"

	includePaths = []



	# Regex patterns
	keyPattern: re.Pattern = re.compile(r"[A-Za-z\_][A-Za-z0-9\_\.]*")

	signsPattern: re.Pattern = re.compile(rf"[{tempSign}{threadSign}]*")

	stepPattern: re.Pattern = re.compile(rf"^(?P<Level>\s*)(?P<Signs>{signsPattern.pattern})(?P<Key>{keyPattern.pattern})((\s*)({delimiter})(\s*)(?P<Value>.*))?(\s*)$")



	# Max level of indentation
	maxLevel = 999



	loopVar: str = "i"



	# Rypple file extensions
	fileExtensions = (
		# Bytecode
		".ryc",
		".rycl",

		# Text Code
		".ryp",
		".rypl",
	)





	@classmethod
	def findFile(cls,name,path,traverse = False):
		paths = [
			path,
			*cls.includePaths
		]


		# Traverse through entire directory
		if (traverse):
			name = "**/" + name


		for path in paths:
			path = Path(path)

			for e in (*cls.fileExtensions, ""):
				# Crate glob pattern
				n = name + e

				for f in path.glob(n):
					# Resolve path
					f = f.resolve()
					
					# Return found path
					return f





	@classmethod
	def readFile(cls,path):
		path = Path(path)

		if (path.is_file()):
			with path.open("rb") as file:
				data = file.read()

				outData = None


				try:
					outData = data[:10].decode("utf-8")
					outData += data[10:].decode("utf-8")

				except:
					outData = data


				steps = cls.parse(outData)
				
				return steps





	@classmethod
	def parse(cls,data):
		# Convert string to steps
		if (isinstance(data,str)):
			lines = cls.toLines(data)
			steps = cls.toSteps(lines)


		# Convert bytecode to steps
		elif (isinstance(data,(bytes,bytearray))):
			steps = Rypple_Step.fromBytecode(data)


		else:
			steps = None


		return steps





	@classmethod
	def validVar(cls,var):
		if (isinstance(var,str)):
			match = cls.keyPattern.fullmatch(var)

			if (match):
				return True

			return False





	@classmethod
	def toLines(cls,data):
		lines = []


		for line in data.split("\n"):
			if (not line.startswith(cls.comment)):
				if (line.strip()):
					lines.append(line)


		return lines





	@classmethod
	def toSteps(cls,lines):
		base = Rypple_Step(
			key = "Base",
			value = None,
			id = -1,
			level = -1,

			temp = False,
			thread = False
		)

		hierarchy = [base]
		previous = base



		for line in lines:
			# Search for line
			match = cls.stepPattern.match(line)



			if (match):
				# Get groups
				levelGroup = match.group("Level")
				signsGroup = match.group("Signs")
				keyGroup = match.group("Key")
				valueGroup = match.group("Value")




				# Get key an value
				key = keyGroup
				value = valueGroup



				if (value != None):
					value = value.strip()


				if (not value):
					value = None



				if (key):
					# Get level
					level = 0
					level += levelGroup.count(" ")
					level += levelGroup.count("\t")



					# Get default signs
					temp = Rypple_Step.temp
					thread = Rypple_Step.thread


					# Temp sign
					if (cls.tempSign in signsGroup):
						temp = not Rypple_Step.temp


					# Thread sign
					if (cls.threadSign in signsGroup):
						thread = not Rypple_Step.thread





					if (level <= cls.maxLevel):
						# All steps that will be processed
						steps = []



						# Create new step
						firstStep = Rypple_Step(
							key = key,
							value = value,
							id = Rypple_Step.newId(),
							level = level,
							
							temp = temp,
							thread = thread,
						)



						# If include step
						if (key == "Include"):
							if (value != None):
								path = cls.findFile(value,".")

								if (path != None):
									if (path.is_file()):
										includeBase = cls.readFile(path)



										# Get import name
										name = path.stem


										# Format import name
										includeBase.key = name


										steps += includeBase.children

						else:
							steps.append(firstStep)



						# Iterate through each step
						for step in steps:
							# Get length of hirarchy
							hlen = len(hierarchy)

							# If the level is beyond the hierarchy extend it
							if (level >= hlen):
								dif = (level - hlen) + 1
								hierarchy += [base] * dif



							# If level is in scope of the previous step
							if (level == previous.level + 1):
								hierarchy[level - 1] = previous



							# Get parent to step
							parent = hierarchy[level - 1]
							if (parent != None):
								parent.addChild(step)



							# Set previous step
							previous = step





		return base






