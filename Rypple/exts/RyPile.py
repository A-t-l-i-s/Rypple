import sys
import os
import subprocess
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

					if (scope.variables.rypile.wait > 0):
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

				args = [scope.variables.rypile.exe]

				for a in scope.variables.rypile.args:
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

					if (scope.variables.rypile.wait > 0):
						process.wait()

				except:
					return Unknown()
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







