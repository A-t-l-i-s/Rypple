from ..types.BaseExtension import *





__all__=["Extension"]





class Extension(BaseExtension):
	enabled=True

	name="Python"

	executable="python.exe"
	extensions=("py","pyw")



	def execute(extension,parent,scope):
		...




	"""
		Description: Sets the input file
		Parameters: path:str[required]
	"""
	class InFile(BaseExtensionKey):
		enabled=True
		name="InFile"

		def callback(extension,parent,scope):
			...





	"""
		Description: Add a lib path
		Parameters: path:str[required]
	"""
	class LibPath(BaseExtensionKey):
		enabled=True
		name="LibPath"


		def callback(extension,parent,scope):
			...





	"""
		Description: Create bytecode files
		Parameters: value:bool[optional]
	"""
	class WriteBytecode(BaseExtensionKey):
		enabled=True
		name="WriteBytecode"


		def callback(extension,parent,scope):
			...




