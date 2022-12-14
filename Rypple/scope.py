import re
import string

from .step import *
from .namespace import *
from .exceptions import *

from .exts.Core import Extension as Core_Extension
from .exts.Console import Extension as Console_Extension





__all__=["Rypple_Scope"]





class Rypple_Scope(object):
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	# Current variables in scope
	variables = Rypple_Namespace({
	})

	constVariables = Rypple_Namespace({
		"char": Rypple_Namespace({
			"endl": "\n",
			"tab": "\t",
			"back": "\b",
		}),

		"step": Rypple_Namespace({
			"current": None,
			"previous": None,
		}),
	})



	# Current import python modules in scope
	modules = Rypple_Namespace({
	})



	# Current extensions loaded in scope
	loadedExtensions = {
		Core_Extension.name: Core_Extension,
	}



	# All available extensions
	extensions = {
		Console_Extension.name: Console_Extension,
	}



	exit = False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Runtime ~~~~~~~~~~~
	def run(self,groups,namespace=None):
		index = 0
		size = len(groups.steps)


		if (namespace == None):
			namespace = self.variables



		while (index < size):
			if (self.exit):
				break


			step = groups.steps[index]
			key = step.key


			# Set Vars
			self.constVariables.step.previous = self.constVariables.step.current
			self.constVariables.step.current = step




			# Find key in extensions
			found = False
			for k,v in self.loadedExtensions.items():
				c = v.get(key)

				if (c != None):
					exc = c.callback(v,step,self,namespace)


					if (isinstance(exc,type) and issubclass(exc,Rypple_Exception)):
						print("Command Error") # Error


					found = True

					break




			# Set a new variable
			if (not found):
				value = self.evaluate(step.value)


				if (self.validVar(key)):
					namespace[key] = value


				else:
					print("Variable Error") # Error




			# Increment step
			index += 1






	def validVar(self,var):
		t = string.ascii_lowercase + string.ascii_uppercase + "_."
		d = string.digits


		if (var):
			for i,c in enumerate(var):
				if (i == 0 and c not in t):
					return False

				elif (c not in t + d):
					return False


			return True
		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~ Evaluate Code ~~~~~~~~
	def evaluate(self,data,file=None):
		# If no file specified
		if (file == None):
			file = "dummy"


		try:
			# Compile data
			comp = compile(data,file,"eval")
	

			# Evaluate data
			out = eval(comp,{
				"defined":self.defined,

				**self.variables.values(),
				**self.constVariables.values(),

				**self.modules.values(),
			},{})
		except:
			out = data


		return out
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ Core Functions ~~~~~~~~
	def defined(self,var):
		if (var in self.namespace or var in self.constVariables):
			return True

		else:
			return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






...