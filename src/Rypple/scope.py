import types
import threading
import traceback

from pathlib import Path

from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from .extensions.core import Extension as Core_Extension
from .extensions.console import Extension as Console_Extension
from .extensions.filesystem import Extension as FileSystem_Extension

from .extensions.rypile import Extension as RyPile_Extension
from .extensions.rypile.c import Extension as RyPile_C_Extension
from .extensions.rypile.cpp import Extension as RyPile_CPP_Extension
from .extensions.rypile.cs import Extension as RyPile_CS_Extension
from .extensions.rypile.java import Extension as RyPile_Java_Extension
from .extensions.rypile.javascript import Extension as RyPile_Javascript_Extension
from .extensions.rypile.kotlin import Extension as RyPile_Kotlin_Extension
from .extensions.rypile.lua import Extension as RyPile_Lua_Extension
from .extensions.rypile.python import Extension as RyPile_Python_Extension

from .extensions.picobridge import Extension as PicoBridge_Extension





__all__ = ("Rypple_Scope",)





class Rypple_Scope:
	# ~~~~~~~~~~ Extensions ~~~~~~~~~~
	extensions = RFT_Structure({
		Console_Extension.name: Console_Extension,
		FileSystem_Extension.name: FileSystem_Extension,

		RyPile_Extension.name: RyPile_Extension,
		RyPile_C_Extension.name: RyPile_C_Extension,
		RyPile_CPP_Extension.name: RyPile_CPP_Extension,
		RyPile_CS_Extension.name: RyPile_CS_Extension,
		RyPile_Java_Extension.name: RyPile_Java_Extension,
		RyPile_Javascript_Extension.name: RyPile_Javascript_Extension,
		RyPile_Kotlin_Extension.name: RyPile_Kotlin_Extension,
		RyPile_Lua_Extension.name: RyPile_Lua_Extension,
		RyPile_Python_Extension.name: RyPile_Python_Extension,

		PicoBridge_Extension.name: PicoBridge_Extension,
	})

	loadedExtensions = RFT_Structure({
		Core_Extension.name: Core_Extension,
	})
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	


	# ~~~~~~~~~~~ Functions ~~~~~~~~~~
	builtins = RFT_Structure({
	})
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	def __init__(self):
		self.variables = RFT_Structure({})


		self.constants = RFT_Structure({
			"dev": RFT_Structure({
				"exit": -1,
				"breakScope": False,
				"file": "dummy",

				"debug": False,

				"enableBytecode": False,
				"enableCommands": True,

				"loopVar": "x",

				"threads": [],
			})
		})


		self.modules = RFT_Structure({
		})


		self.loadedExtensions = RFT_Structure(
			Rypple_Scope.loadedExtensions
		)


		self.exceptionLevel = 1





	# ~~~~~~~~~~ Compilation ~~~~~~~~~
	@RFT_Name("run")
	@RFT_Description("""
		Compiles Rypple_Steps in the current scope

		@base : Rypple_Step = The first step to be compiled usually the base of children steps
		@namespace : Rypple_Namespace = Optional but sets the current scope of the variable being set to (Do not use to start)

		@return : bool = Whether the program exiting properly wihtout any critical errors
	""")
	def run(self, base, namespace = None):
		index = 0
		size = len(base.children)


		# If namespace is none
		if (namespace == None):
			namespace = self.variables


		while (index < size):
			# If exit var is anything but -1
			if (self.constants.dev.exit != -1):
				return False

			# If break loop
			if (self.constants.dev.breakScope):
				self.constants.dev.breakScope = False
				return False


			# Get step and key
			step = base.children[index]
			key = step.key


			# Set constant step
			self.constants.dev.step = step



			if (self.constants.dev.enableCommands):
				if (step.command):
					for k,v in self.loadedExtensions.items():
						# Get command
						command = v.get(step.key)


						if (command != None):
							# Call command
							self.callFunction(
								func = command,
								args = (),
								kwargs = {
									"cls": v,
									"step": step,
									"scope": self,
									"namespace": namespace
								},
								thread = step.thread
							)

							# Break loop
							break



			if (not step.command):
				if (len(step.children) > 0):
					# Create new namespace
					newNamespace = RFT_Structure({})

					# Add new namespace
					self.setVar(key, newNamespace, namespace = namespace)

					# Run new namespace
					self.callFunction(
						func = self.run,
						args = (
							step,
						),
						kwargs = {
							"namespace": newNamespace
						},
						thread = step.thread
					)



				else:
					if (step.value != None):
						# Evaluate and set variable
						self.callFunction(
							func = self.evaluateVar,
							args = (
								key,
								step.value,
								namespace
							),
							kwargs = {},
							thread = step.thread
						)



			# Increment step
			index += 1


		return True
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Evaluation ~~~~~~~~~~
	@RFT_Name("evaluate")
	@RFT_Description("""
		Evaluates string representations of values

		@data : str = String representation of a value
		@namespace : RFT_Structure = Optional but sets the current scope of the variable being set to

		@return: null
	""")
	def evaluate(self, data:str, namespace:RFT_Structure = None):
		if (isinstance(data, str)):
			if (namespace == None):
				namespace = RFT_Structure({})


			# Define exc
			exc = None


			try:
				dataCompile = compile(
					data,
					self.constants.dev.file,
					"eval"
				)


				outData = eval(
					dataCompile,
					{
						"__annotations__": {},
						"__builtins__": self.builtins.data(),

						**self.variables.data(),
						**self.constants.data(),
						**namespace.data(),
						**self.modules.data(),
					},
					{}
				)

			except:
				# Get formated exception
				exc = RFT_Exception(
					traceback.format_exc(),
					RFT_Exception.ERROR
				)

				outData = None

			finally:
				if (exc != None):
					if (exc.level <= self.exceptionLevel or self.exceptionLevel <= 0):
						# Output exception
						print(
							exc.message()
						)
		else:
			outData = data


		return outData





	@RFT_Name("evaluateVar")
	@RFT_Description("""
		Evauates and sets variable as the evaluate value

		@key : str = Variable name
		@data : str = String representation of a value
		@namespace : RFT_Structure = Optional but sets the current scope of the variable being set to

		@return : null
	""")
	def evaluateVar(self, key:str, data:str, namespace:RFT_Structure = None):
		# Evaluate data
		value = self.evaluate(
			data,
			namespace = namespace
		)

		# Set var
		self.setVar(
			key,
			value,
			namespace = namespace
		)





	@RFT_Name("setVar")
	@RFT_Description("""
		Sets a variable into the scope accordingly
		Check if variable exists in global scope and determine if it's a namespace then set that variable
		
		@key : str = Variable name
		@value : any = The value the variable is setting
		@namespace : RFT_Structure = Optional but sets the current scope of the variable being set to
		
		@return : null
	""")
	def setVar(self, key:str, value, namespace:RFT_Structure = None):
		if (namespace == None):
			namespace = self.variables


		# Split key
		path = key.split(".")
		var = path.pop(-1)


		try:
			parent = namespace.parent(key)
		except:
			if (len(path) > 0):
				parent = namespace.allocate(path)

			else:
				parent = namespace


		# Set var
		parent[var] = value
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Threads ~~~~~~~~~~~
	@RFT_Name("callFunction")
	@RFT_Description("""
		Calls a function and logs its progress if debug is True

		@func : function = The function being called
		@args : list/tuple = Normal arguments
		@kargs : dict = Keyword arguments
		@thread : bool = If thread shold be ran in a seperate thread

		@return : null
	""")
	def callFunction(self, func, args:list = (), kwargs:dict = {}, thread:bool = False):
		if (thread):
			# Create new thread
			newThread = threading.Thread(
				target = self.callFunction,
				args = (
					func,
					args,
					kwargs
				),
				kwargs = {
					"thread": False
				},
				daemon = True
			)

			# Append thread to list of all running threads
			self.constants.dev.threads.append(
				newThread
			)

			# Start thread
			newThread.start()



		else:
			retValue = None

			try:
				# Call function
				retValue = func(
					*args,
					**kwargs
				)


			except RFT_Exception as exc:
				# Output exception
				retValue = exc


			except:
				# Get formated exception
				retValue = RFT_Exception(
					traceback.format_exc(),
					RFT_Exception.ERROR
				)


			finally:
				if (isinstance(retValue, (types.GeneratorType, RFT_Exception))):
					if (isinstance(retValue, RFT_Exception)):
						retValue = (retValue,)

					for x in retValue:
						if (isinstance(x, RFT_Exception)):
							if (x.level <= self.exceptionLevel or self.exceptionLevel <= 0):
								print(
									x.message()
								)

				return retValue





	@RFT_Name("wait")
	@RFT_Description("""
		Wait and join all scope threads to finish before closing

		@return : null
	""")
	def wait(self):
		# Iterate until all threads are closed
		for t in self.constants.dev.threads:
			# Join thread
			t.join()


		# Clear threads list
		self.constants.dev.threads.clear()





	@RFT_Name("loadExtension")
	@RFT_Description("""
		Loads a new extension into current scope

		@name : str = Name of extension being loaded

		@return : null
	""")
	def loadExtension(self, name:str):
		# If extension exists
		if (self.extensions.contains(name)):
			# Get extension
			ext = self.extensions[name]

			# Load extension
			ext.init(
				ext,
				self
			)

			self.loadedExtensions[name] = ext
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






