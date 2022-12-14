import os
import shlex
import ntpath

from ..BaseExtension import *





__all__=["Extension"]





class Extension(BaseExtension):
	enabled=True

	name="Python"

	executable="python.exe"
	extensions=("py","pyw")



	def execute(extension,parent,scope):
		args=parent.removeNone([
			extension.executable,
			scope["py_infile"],

			*scope.extra
		])

		parent.process(scope,args)




	"""
		Description: Sets the input file
		Parameters: path:str[required]
	"""
	class InFile(BaseExtensionKey):
		enabled=True
		name="InFile"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)

			if (isinstance(value,str)):
				if (ntpath.exists(value) and ntpath.isfile(value)):
					scope["py_infile"]=value

				else:
					... # Error
			else:
				... # Error





	"""
		Description: Add a lib path
		Parameters: path:str[required]
	"""
	class LibPath(BaseExtensionKey):
		enabled=True
		name="LibPath"


		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,(list,tuple))):
				value=";".join(value)


			if (isinstance(value,str)):
				scope.updateEnv("PYTHONPATH",";" + value)

			else:
				... # Error





	"""
		Description: Create bytecode files
		Parameters: value:bool[optional]
	"""
	class WriteBytecode(BaseExtensionKey):
		enabled=True
		name="WriteBytecode"


		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,bool)):
				if (value):
					scope.setEnv("PYTHONDONTWRITEBYTECODE","1")

				else:
					scope.setEnv("PYTHONDONTWRITEBYTECODE","0")


			elif (value == None):
					scope.setEnv("PYTHONDONTWRITEBYTECODE","1")


			else:
				... # Error




