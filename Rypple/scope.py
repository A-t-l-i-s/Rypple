import re
import string

from .step import *
from .namespace import *
from .exceptions import *

from .exts.Core import Extension as Core_Extension
from .exts.Console import Extension as Console_Extension

from .exts.RyPile import Extension as RyPile_Extension
from .exts.Python import Extension as Python_Extension





__all__=["Rypple_Scope"]





class Rypple_Scope(object):
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	# Current variables in scope
	variables = Rypple_Namespace({
	})

	constants = Rypple_Namespace({
		"step": Rypple_Namespace({
			"current": None,
			"previous": None,
		}),

		"char": Rypple_Namespace({
			"endl": "\n",
			"tab": "\t",
			"back": "\b",
		}),

		"exit": False,
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
		
		RyPile_Extension.name: RyPile_Extension,
		Python_Extension.name: Python_Extension,
	}
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Runtime ~~~~~~~~~~~
	def run(self,groups,namespace=None):
		index = 0
		size = len(groups.steps)


		if (namespace == None):
			namespace = self.variables



		while (index < size):
			if (self.constants.exit):
				break


			step = groups.steps[index]
			key = step.key


			# Set Vars
			self.constants.step.previous = self.constants.step.current
			self.constants.step.current = step




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
				value = self.evaluate(step.value,namespace)


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





	def loadExtension(self,val):
		if (val in self.extensions):
			if (val not in self.loadedExtensions):
				ext = self.extensions[val]

				try:
					ext.init(ext,self)
								
				except:
					...

				finally:
					self.loadedExtensions[ext.name] = ext
					return True

		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~ Evaluate Code ~~~~~~~~
	def evaluate(self,data,namespace=None,file=None):
		# If no file specified
		if (file == None):
			file = "dummy"


		if (namespace == None or namespace == self.variables):
			namespace = Rypple_Namespace()


		try:
			# Compile data
			comp = compile(data,file,"eval")

	

			# Evaluate data
			out = eval(comp,{
				"defined":self.defined,

				**namespace.values(),
				**self.variables.values(),
				**self.constants.values(),

				**self.modules.values(),
			},{})
		except:
			out = data


		return out
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ Core Functions ~~~~~~~~
	def defined(self,var):
		if (var in self.namespace or var in self.constants):
			return True

		else:
			return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



