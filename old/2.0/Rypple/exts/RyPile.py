import sys
import os
import subprocess
from pathlib import Path
from typing import Iterable

from ..extension import *
from ..namespace import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "RyPile"
	enabled = True



	def init(cls,scope):
		scope.variables.rypile = Rypple_Namespace({
				"popout": False,
				"wait": True,
				"args": [],
				"exe": None,
				"env": dict(os.environ),
				"ext": None,
			},
			True
		)





	"""
		Description: ...
		Parameters: ...
	"""
	class Run(Rypple_ExtensionKey):
		name = "Run"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					val = (value,)

				elif (isinstance(value,Iterable)):
					val = tuple(value)

				else:
					return Unknown()



				args = []

				for a in val:
					args.append(str(a))



				if (scope.variables.rypile.popout):
					creationFlags = subprocess.CREATE_NEW_CONSOLE

				else:
					creationFlags = 0x00


				try:
					process = subprocess.Popen(
						args,
						creationflags=creationFlags,
						env=scope.variables.rypile.env
					)

					if (scope.variables.rypile.wait):
						process.wait()

				except:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Done(Rypple_ExtensionKey):
		name = "Done"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (not step.isCmd()):
				# If extension as loaded
				ext = scope.variables.rypile.ext

				if (issubclass(ext,Rypple_Extension)):
					if (ext.name in scope.loadedExtensions):
						scope.variables.rypile.ext = None

						scope.loadedExtensions.pop(ext.name)



				# Set args
				args = [scope.variables.rypile.exe]



				# Iterate through rypile args
				for a in scope.variables.rypile.args:
					args.append(str(a))



				# If popout program
				if (scope.variables.rypile.popout):
					creationFlags = subprocess.CREATE_NEW_CONSOLE

				else:
					creationFlags = 0x00



				# Create new process
				try:
					process = subprocess.Popen(
						args,
						creationflags=creationFlags,
						env=scope.variables.rypile.env
					)

					if (scope.variables.rypile.wait):
						process.wait()

				except:
					return Unknown()


				# Clear args
				scope.variables.rypile.args.clear()
			
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Extra(Rypple_ExtensionKey):
		name = "Extra"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					args = (value,)

				elif (isinstance(value,Iterable)):
					args = tuple(value)

				else:
					return Unknown()


				scope.variables.rypile.args += args

			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Reset(Rypple_ExtensionKey):
		name = "Reset"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (not step.isCmd()):
				scope.variables.rypile.args.clear()

			else:
				return Unknown()




	"""
		Description: ...
		Parameters: ...
	"""
	class Directory(Rypple_ExtensionKey):
		name = "Directory"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)

				if (isinstance(value,str)):
					path = Path(value)

					if (path.is_dir()):
						os.chdir(path)

					else:
						return Unknown()
				else:
					return Unknown()
			else:
				return Unknown()







