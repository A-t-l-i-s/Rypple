import re
import os
import uuid
import zlib
import ntpath
import pickle
from pathlib import Path

from .path import *
from .scope import *
from .step import *
from .encoder import *
from .namespace import *

from .exts.Core import Extension as Core_Extension





__all__=["Rypple","Rypple_Scope","Rypple_JSON_Encoder","loads","load"]





# ~~~~~~~~~~~~ Rypple ~~~~~~~~~~~~
class Rypple:
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	fileExtensions = (
		".ryp",
		".rypl",
		".ryc",
		".rycl",
	)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	"""
		Searches for specified file name in paths
	"""
	def searchFile(self,name,paths_=()):
		paths = []
		for p in paths_:
			if (isinstance(p,str)):
				if (ntpath.exists(p)):
					if (ntpath.isfile(p)):
						paths.append(ntpath.dirname(p))

					else:
						paths.append(p)


		paths += os.environ.get("PATH","").split(";")
		paths += os.environ.get("RYPPLE_MODULES","").split(";")

		paths += (
			"./modules",
		)

		for p in paths:
			for e in self.fileExtensions + ("",):
				p_ = ntpath.join(p,name + e)
				p_ = ntpath.realpath(p_)

				if (ntpath.exists(p_) and ntpath.isfile(p_)):
					return p_





	"""
		Read file and parse into steps
	"""
	def parseFile(self,path):
		steps = []
		
		if (isinstance(path,str)):
			if (ntpath.exists(path) and ntpath.isfile(path)):
				with open(path,"rb") as file:
					buffer = file.read()


				try:
					data = buffer.decode()

				except:
					data = buffer


				steps = self.parseData(data)


		return steps





	"""
		Parse data into steps
	"""
	def parseData(self,data):
		if (isinstance(data,str)):
			lines = data.split("\n")

			steps = self.parseLines(lines)
			groups = self.parseSteps(steps)

			return groups




		elif (isinstance(data,(bytes,bytearray))):
			groups = Rypple_Step.fromBytecode(data)

			return groups




		return None





	"""
		Takes in unfiltered lines as list and parses them into a filtered list of steps
	"""
	def parseLines(self,lines):
		steps=[]


		# Iterate through all lines
		for line in lines:
			# Declare vars
			key = None
			value = None
			level = -1


			# Search for statement in line
			v = re.search(r"^\s*[a-zA-Z\_]{1}[a-zA-Z0-9\.\_]*\s*$",line)



			# If found a statement in line
			if (v):
				f,t = v.span()
				
				key = line[:t]
				value = None
				level = key.count("\t") + key.count(" ")

				# Clean key
				key = key.strip()


			else:
				# Search for command in line
				v = re.search(r"^\s*[a-zA-Z\_]{1}[a-zA-Z0-9\.\_]*\s*:",line)


				# If found a command in line
				if (v):
					f,t = v.span()

					key = line[f:t]
					value = line[t:]
					level = key.count("\t") + key.count(" ")

					# Clean key
					key = key.strip()
					key = key.rstrip(":")
					key = key.strip()

					# Clean value
					value = value.strip()




			if (key):
				# Create step model
				step = Rypple_Step(
					key = key,
					value = value,
					level = level,
					id = uuid.uuid1().int,
				)

				steps.append(step)


		return steps





	"""
		Takes in steps and groups them into according scopes
	"""
	def parseSteps(self,steps):
		blocks = Rypple_Step(key="Base")
		block = blocks
		previousBlocks = [block]

		index = 0





		while (index < len(steps)):
			step = steps[index]
			
			key = step.key
			value = step.value

			step.parent = block.id



			# Create new group
			if (key in (
					Core_Extension.If.name,
					Core_Extension.Function.name,
					Core_Extension.For.name,
					Core_Extension.While.name,
					Core_Extension.Namespace.name,
					Core_Extension.Else.name
				)):
				
				block.steps.append(step)
				previousBlocks.append(block)

				block = step



			# Stepback from current group
			elif (key == Core_Extension.End.name):
				if (value == None):
					if (len(previousBlocks) > 0):
						block = previousBlocks.pop(-1)

				else:
					... # Error



			# Include code from other files
			elif (key == Core_Extension.Include.name):
				if (value != None):
					steps.pop(index)


					if (isinstance(value,str)):
						p = self.searchFile(value,())


						if (p != None):
							groups = self.parseFile(p)


							for s in groups.steps[::-1]:
								block.steps.insert(index,s)

						else:
							... # Error
					else:
						... # Error


					index -= 1

				else:
					... # Error



			# Ignore these commands
			elif (key == Core_Extension.Pass.name):
				if (value == None):
					...

				else:
					... # Error




			else:
				block.steps.append(step)




			index += 1




		return blocks













def loads(data,scope = None):
	r = Rypple()


	# Parse groups
	groups = r.parseData(data)


	# Create new scope
	if (not isinstance(scope,Rypple_Scope)):
		scope = Rypple_Scope()
	

	scope.run(groups)

	var = scope.variables
	var.removeTemps()

	return var





def load(path,scope = None):
	r = Rypple()


	# Parse groups
	groups = r.parseFile(path)


	# Create new scope
	if (not isinstance(scope,Rypple_Scope)):
		scope = Rypple_Scope()


	scope.constants.file.path = Path(path).resolve()
	

	scope.run(groups)

	var = scope.variables
	var.removeTemps()

	return var












