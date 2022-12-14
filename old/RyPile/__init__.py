import re
import uuid
import ntpath

from .scope import *

from .types.BaseExtension import *

from .extensions.Core import Extension as Core_Extension
from .extensions.Python import Extension as Python_Extension





__all__=["RyPile","RyPile_Scope"]





class RyPile:
	

	extensions=("","rypl")


	# Constants
	COMMAND=0
	STATEMENT=1


	# Regular exprssions
	varRegex=				r"\@\[\s*{var}+\s*\]"
	commandRegex=			r"^\s*[\w\d\.\-\_]{1,256}:"
	statementRegex=			r"^\s*[\w\d\.\-\_]{1,256}$"

	scopeCmds=[]
	takeawayCmds=[]






	def __init__(self):
		...





	def parseLine(self,line):
		# Declare vars
		key=None
		value=None
		level=-1


		# Search for statement in line
		v=re.search(self.statementRegex,line)


		if (v):
			f,t=v.span()
			
			key=line[:t]
			value=None
			level=key.count("\t") + key.count(" ")

			key=key.lstrip()


		else:
			# Search for command in line
			v=re.search(self.commandRegex,line)


			if (v):
				f,t=v.span()

				key=line[f:t]
				value=line[t:]
				level=key.count("\t") + key.count(" ")

				key=key.lstrip()
				key=key.rstrip(":")
				value=value.strip()




		if (key != None):
			if (value != None):
				t=RyPile.COMMAND
			else:
				t=RyPile.STATEMENT


			d={
				"type":t,
				"key":key,
				"value":value,
				"level":level,
				"id":uuid.uuid1().int,
				"file":None,
				"steps":[],
			}



			return d

		else:
			return None





	def parseSteps(self,steps):
		blocks={"key":"","steps":[]}
		block=blocks
		previous=[block]

		i=0


		while (i < len(steps)):
			s=steps[i]

			k=s["key"]


			if (k in ["If","Elif","Else","Function","For","Foreach","While"]):
				if (k in ["Elif","Else"]):
					if (len(previous) > 0):
						block=previous.pop(-1)


				block["steps"].append(s)

				previous.append(block)
				
				block=s



			elif (k == "End"):
				if (len(previous) > 0):
					block=previous.pop(-1)



			else:
				block["steps"].append(s)



			i+=1


			
		return blocks







	def parseFile(self,path):
		steps=[]

		for ext in self.extensions:
			p=ntpath.realpath(path + "." + ext)

			if (ntpath.exists(p) and ntpath.isfile(p)):
				with open(p,"r") as f:
					for l in f.readlines():
						s=self.parseLine(l)

						if (s != None):
							s["file"]=p

							steps.append(s)


				break


		return steps










