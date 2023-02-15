import sys
import re
import copy
import math
import threading
import traceback
import importlib, importlib.util
from pathlib import Path

from .__init__ import *
from .namespace import *
from .exceptions import *





__all__ = ("Rypple_Scope",)





class Rypple_Scope:
	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	# Extensions
	extensions: list = {}

	# Loaded extension
	loadedExtensions: list = {}



	# Builtin functions
	builtins: dict = {
		# ~~~~~ Vars ~~~~~
		"__name__": 		None,



		# ~~~~~ Misc ~~~~~
		"dir": 				dir,
		"type": 			type,



		# ~~~~~ Data Types ~~~~~
		"hex": 				hex,
		"oct": 				oct,



		# ~~~~~ Lists ~~~~~
		"filter": 			filter,
		"format": 			format,
		"len": 				len,
		"next": 			next,
		"reversed": 		reversed,
		"sorted": 			sorted,



		# ~~~~~ Boolean ~~~~~
		"all": 				all,
		"any": 				any,
		"isinstance": 		isinstance,
		"issubclass": 		issubclass,



		# ~~~~~ Attributes ~~~~~
		"delattr": 			delattr,
		"getattr": 			getattr,
		"hasattr": 			hasattr,
		"setattr": 			setattr,



		# ~~~~~ Math ~~~~~
		"abs": 				abs,
		"divmod": 			divmod,
		"max": 				max,
		"min": 				min,
		"pow": 				pow,
		"round": 			round,
		"sum": 				sum,

		"sqrt": 			math.sqrt,
		"ceil": 			math.ceil,
		"floor": 			math.floor,
		"cos": 				math.cos,
		"sin": 				math.sin,
		"tan": 				math.tan,
		"rad": 				math.radians,
		"deg": 				math.degrees,

		"inf": 				math.inf,
		"nan": 				math.nan,
		"pi": 				math.pi,



		# ~~~~~ Types ~~~~~
		"ascii": 			ascii,
		"bin": 				bin,
		"bool": 			bool,
		"bytearray": 		bytearray,
		"bytes": 			bytes,
		"complex": 			complex,
		"dict": 			dict,
		"enumerate": 		enumerate,
		"float": 			float,
		"iter": 			iter,
		"list": 			list,
		"map": 				map,
		"object": 			object,
		"range": 			range,
		"repr": 			repr,
		"set": 				set,
		"slice": 			slice,
		"str": 				str,
		"tuple": 			tuple,
		"zip": 				zip,
	}
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Initialize ~~~~~~~~~~
	def __init__(self):
		# Variables
		self.variables: Rypple_Namespace = Rypple_Namespace({
		})



		# Constants
		self.constants: Rypple_Namespace = Rypple_Namespace({
			"exit": -1,
			"step": None,
			"file": "dummy",

			"debug": False
		})



		# Loaded modules
		self.modules: Rypple_Namespace = Rypple_Namespace({
		})



		# Re-initialize extensions
		self.loadedExtensions = dict(Rypple_Scope.loadedExtensions)



		# Threads
		self.threads:list = []
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Compilation ~~~~~~~~~
	def run(self,base,*,namespace=None):
		index = 0
		size = len(base.children)



		# If namespace is none set it to global
		if (namespace == None):
			namespace = self.variables



		while (index < size):
			# If exit code is greater than -1 exit program
			if (self.constants.exit > -1):
				break



			# Get step
			step = base.children[index]
			key = step.key

			# Set constant step
			self.constants.step = step



			# Find key in extensions
			foundExtension = False

			for k,v in self.loadedExtensions.items():
				# Get command
				command = v.get(key)

				# If command is present
				if (command != None):
					foundExtension = True


					# Call command
					self.callFunction(
						command,
						(
							v,
							step,
							self,
							namespace
						),
						{},
						thread = step.thread
					)


					break




			if (not foundExtension):
				if (step.hasChildren()):
					# Create new namespace
					newNamespace = Rypple_Namespace({"__temp__": step.temp})

					# Add namespace to parent
					namespace[key] = newNamespace



					# Run in new namespace
					self.callFunction(
						self.run,
						(
							step,
						),
						{
							"namespace": newNamespace
						},
						thread = step.thread
					)




				else:
					if (step.value != None):
						# Evaluate and set variable
						self.callFunction(
							self.evaluateVar,
							(
								key,
								step.value,
								namespace
							),
							{},
							thread = step.thread
						)



			# Increment step
			index += 1
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Evaluation ~~~~~~~~~~
	def evaluate(self,data,*,namespace=None):
		if (isinstance(data,str)):
			# If namespace is none
			if (namespace == None):
				namespace = Rypple_Namespace()


			try:
				# Compile data
				dataCompile = compile(data,self.constants.file,"eval")


				# Evaluate data
				outData = eval(dataCompile,{
					"__annotations__": {},
					"__builtins__": self.builtins,

					**self.variables.values(),
					**self.constants.values(),
					**namespace.values(),
					**self.modules.values()
				},{})


			except:
				# Default to string out
				outData = data

		else:
			outData = data


		return outData





	def evaluateVar(self,key,data,namespace):
		# Evaluate data
		value = self.evaluate(
			data,
			namespace = namespace
		)

		# Set var
		namespace[key] = value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Threads ~~~~~~~~~~~
	def callFunction(self,func,args,kwargs,*,thread=False):
		if (thread):
			# Create thread
			newThread = threading.Thread(
				target = self.callFunction,
				args = (
					func,
					args,
					kwargs
				),
				kwargs = {
					"thread": False,
				},
				daemon = True
			)


			# Add thread to list
			self.threads.append(newThread)


			# Run thread
			newThread.start()




		else:
			try:
				# Call function
				ret = func(
					*args,
					**kwargs
				)

			except:
				ret = Rypple_Error(f"Failed to run '{func.__name__}'\n{traceback.format_exc()}")



			# If return type is an exception
			if (isinstance(ret,Rypple_Exception)):

				# If in debug mode
				if (self.constants.debug):
					
					# Write data to stdout
					sys.stdout.write(ret.text + "\n")


				# Exit program if citical error
				if (isinstance(ret,Rypple_Critical)):
					self.constants.exit = 1






	def wait(self):
		# Iterate until all threads are closed
		for t in self.threads:
			# Join thread
			t.join()


		# Clear threads list
		self.threads.clear()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Methods ~~~~~~~~~~~
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~












# ~~~~~~~~ Load Extensions ~~~~~~~
# Get file path
filePath = Path(__file__)

# Get extensions path
extensionsPath = (filePath.parent / "extensions").resolve()



# Get extension path files
for f in extensionsPath.rglob("*.py"):
	# Resolve file path
	f = f.resolve()



	# Get name and format it
	nameFmt = f.as_posix().replace(extensionsPath.as_posix(),"")
	nameFmt = nameFmt.rstrip(".py")
	nameFmt = nameFmt.strip("\\")
	nameFmt = nameFmt.replace("/","\\")



	# Split name between the delimiters
	nameSplit = nameFmt.split("\\")



	# If namesplit is greater than 1
	if (len(nameSplit) > 1):
		# If it ends with core than its a parent
		if (nameSplit[-1].lower() == "core"):
			nameSplit.pop(-1)



	# Join name
	name = ".".join(nameSplit)
	name = name.strip(".")



	# Import module spec
	spec = importlib.util.spec_from_file_location(name,f)

	# Get module
	module = importlib.util.module_from_spec(spec)



	try:
		# Compile module
		spec.loader.exec_module(module)

	except:
		...



	if (hasattr(module,"Extension")):
		# Get module extension
		ext = module.Extension


		# Get meta data
		name = ext.name
		description = ext.description
		enabled = ext.enabled
		core = ext.core


		# Add extension to extension list
		if (core):
			if (enabled):
				Rypple_Scope.loadedExtensions[name] = ext

		else:
			Rypple_Scope.extensions[name] = ext
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~







