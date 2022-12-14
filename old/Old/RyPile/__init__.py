import sys
import re
import os
import json
import uuid
import ntpath
import subprocess

from .BaseExtension import *

from .exts.Core import Extension as Core_Extension
from .exts.Python import Extension as Python_Extension





__all__=["RyPile","RyPile_Scope"]





class RyPile:



	extensions={
		Python_Extension.name: Python_Extension,
	}



	def __init__(self):
		...





	# ~~~~~~~~~~~~ Parsers ~~~~~~~~~~~
	# Get steps from file path
	def getSteps(self,path):
		steps=[]


		if (ntpath.exists(path) and ntpath.isfile(path)):
			path=ntpath.realpath(path)


			# Open input file
			inputFile=open(
				file=path,
				mode="r",
			)


			i=0
			for lineNum,line in enumerate(inputFile.readlines()):
				if (line):
					# Convert line to step
					key,value=self.splitStep(line)

					if (key!=None):
						i+=1


						# Add step to list of steps
						steps.append({
							"key":key,
							"value":value,
							"line":lineNum,
							"file":path,
							"id":uuid.uuid1(),
						})


			inputFile.close()


		return steps



	# Split line into key and value
	def splitStep(self,line):
		# Variables
		key=""
		value=""
		pastName=False


		line=line.strip()


		if (line):
			for i,c in enumerate(line):
				# If its past the name definition
				if (pastName):
					value+=c
				else:
					# If character is not a number/letter/space
					if (c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."):
						# If reached delimeter
						if (c == ':'):
							pastName=True
						else:
							key=None
							break
					else:
						key+=c



			if (not key):
				key=None
			
			else:
				key=key.strip()


			if (pastName):
				value=value.strip()

			else:
				value=None


			return key,value
		return None,None
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




	# ~~~~~~~~~~~~ Compile ~~~~~~~~~~~
	def run(self,scope,steps):
		if (len(steps) > 0):
			f=ntpath.realpath(steps[0]["file"])
			p=ntpath.dirname(f)


			if (ntpath.exists(p) and ntpath.isdir(p)):

				# Change directory to file path
				os.chdir(p)
				scope.path=p
				

				# Add steps to scope
				scope.steps+=steps


				while (scope.index < len(scope.steps)):
					# Exit loop
					if (scope.exit):
						break



					# Get step
					step=scope.steps[scope.index]

					ext=scope.extension



					# Get vars
					key=step["key"]
					value=step["value"]
					line=step["line"]
					file=step["file"]



					# If key is a core statement
					if ((coreKey:=Core_Extension.get(key)) != None):
						# If enabled
						if (coreKey.enabled):
							# Callback core key
							coreKey.callback(Core_Extension,self,scope,step)



					# If key is an extension statement
					elif (ext!=None and (extKey:=ext.get(key)) != None):
						# If enabled
						if (ext.enabled):
							# Callback extension key
							extKey.callback(ext,self,scope,step)



					# Key is just used to assign a variable
					else:
						value=scope.format(value)
						value=scope.evaluate(value)

						scope[key]=value



					# Increment step index
					scope.index+=1
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Functions ~~~~~~~~~~
	# Create a process
	def process(self,scope,args):
		# No creation flags
		creationFlags=0x00


		# Decide if it should create a new console
		if (scope.popout):
			creationFlags=subprocess.CREATE_NEW_CONSOLE


		try:
			p=subprocess.Popen(
				args,
				env=scope.env,
				creationflags=creationFlags,
			)

			p.wait()

			return True
		except:
			return False




	# Filter all nones froom list
	def removeNone(self,args):
		l=[]
		for a in args:
			if (not isinstance(a,(tuple,list))):
				a_=[a]

			else:
				a_=a


			if (None not in a_):
				l.append(a)


		return l
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~









# Class to define a rypile scope 
class RyPile_Scope:



	data={
	}


	index=0
	path=None
	extra=[]
	steps=[]
	popout=False
	extension=None
	exit=False
	calls=[]
	env=dict(os.environ)



	def __init__(self):
		...





	# ~~~~~~~~~~ Dictionary ~~~~~~~~~~
	def __getitem__(self,key):
		if (not isinstance(key,tuple)):
			key=(key,None)


		return self.data.get(*key)



	def __setitem__(self,key,data):
		self.data[key]=data
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	# ~~~~~~~~~~ Converters ~~~~~~~~~~
	# Format string to include variables
	def format(self,data):
		if (isinstance(data,str)):
			d=dict(self.data)


			for k,v in d.items():
				data=re.sub(
					rf"\@\[\s*{k}\s*\]",
					str(v).replace("\\","\\\\"),
					data,
				)



			return data.strip()

		return data
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~ Evaluate Conditions ~~~~~
	def evaluate(self,data):
		if (isinstance(data,str)):
			try:
				ret=eval(data,{
					"defined":self.defined,
				},{})

				return ret
			except:
				...


		return data




	def defined(self,key):
		return key in self.data.keys()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~~ Lines ~~~~~~~~~~~~
	# Find line by uuid
	def findLine(self,uid):
		for i,s in enumerate(self.steps):
			if (s["id"] == uid):
				return i,s


		return -1,None





	def skipTo(self,key):
		if (isinstance(key,str)):
			key=[key]

		while (True):
			self.index+=1

			i=self.index

			if (i<len(self.steps)):
				s=self.steps[i]


				if (s["key"] in key):
					return True

			else:
				break


		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~ Environment Vars ~~~~~~~
	def setEnv(self,key,value):
		key=str(key)
		value=str(value)

		self.env[key]=value



	def updateEnv(self,key,value):
		key=str(key)
		value=str(value)

		self.env[key]=self.env.get(key,"") + value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





