from ..types.BaseExtension import *





__all__=["Extension"]





class Extension(BaseExtension):
	enabled=True

	name="Core"

	executable=None
	extensions=()



	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	"""
		Description: Sets the current directory
		Parameters: path:str[required]
	"""
	class Path(BaseExtensionKey):
		enabled=True
		name="Path"

		def callback(extension,parent,scope):
			...





	"""
		Description: Adds extra arguments to the extension
		Parameters: args:list[str][required]
	"""
	class Extra(BaseExtensionKey):
		enabled=True
		name="Extra"

		def callback(extension,parent,scope):
			...





	"""
		Description: Specifies if any external processes are created with a new console
		Parameters: value:bool[required]
	"""
	class Popout(BaseExtensionKey):
		enabled=True
		name="Popout"

		def callback(extension,parent,scope):
			...





	"""
		Description: Specifies the current extension
		Parameters: ext:str[required]
	"""
	class Extension(BaseExtensionKey):
		enabled=True
		name="Extension"

		def callback(extension,parent,scope):
			...





	"""
		Description: Specifies the extension executable
		Parameters: path:str[required]
	"""
	class Executable(BaseExtensionKey):
		enabled=True
		name="Executable"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Commands ~~~~~~~~~~~
	"""
		Description: Pauses the compilation process to start a new external process
		Parameters: args:list[str][required]
	"""
	class Run(BaseExtensionKey):
		enabled=True
		name="Run"

		def callback(extension,parent,scope):
			...





	"""
		Description: Delays the compilation process at the current line
		Parameters: secs:float[required]
	"""
	class Delay(BaseExtensionKey):
		enabled=True
		name="Delay"

		def callback(extension,parent,scope):
			...




	"""
		Description: Adds steps from specified file into the current scope
		Parameters: path:str[required]
	"""
	class Include(BaseExtensionKey):
		enabled=True
		name="Include"

		def callback(extension,parent,scope):
			...





	"""
		Description: Deletes variable from scope
		Parameters: var:str[required]
	"""
	class Delete(BaseExtensionKey):
		enabled=True
		name="Delete"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Statements ~~~~~~~~~~
	"""
		Description: Compiles current extension
		Parameters: None
	"""
	class Done(BaseExtensionKey):
		enabled=True
		name="Done"

		def callback(extension,parent,scope):
			...





	"""
		Description: Exit breaks the compilation loop
		Parameters: None
	"""
	class Exit(BaseExtensionKey):
		enabled=True
		name="Exit"

		def callback(extension,parent,scope):
			...





	"""
		Description: Ignores this step
		Parameters: None
	"""
	class Pass(BaseExtensionKey):
		enabled=True
		name="Pass"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	


	# ~~~~~~~~~~~~ Console ~~~~~~~~~~~
	"""
		Description: Prints data to the console
		Parameters: text:str[required]
	"""
	class Print(BaseExtensionKey):
		enabled=True
		name="Print"

		def callback(extension,parent,scope):
			...





	"""
		Description: Clears the console
		Parameters: None
	"""
	class Clear(BaseExtensionKey):
		enabled=True
		name="Clear"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Conditions ~~~~~~~~~~
	"""
		Description: Conditional if statement
		Parameters: condition:str[required]
	"""
	class If(BaseExtensionKey):
		enabled=True
		name="If"

		def callback(extension,parent,scope):
			...





	"""
		Description: Conditional else statement
		Parameters: None
	"""
	class Else(BaseExtensionKey):
		enabled=True
		name="Else"

		def callback(extension,parent,scope):
			...





	"""
		Description: Signals that the end of the if/for/while/function statement
		Parameters: None
	"""
	class End(BaseExtensionKey):
		enabled=True
		name="End"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Function ~~~~~~~~~~~
	"""
		Description: Declares a callable function
		Parameters: name:str[required]
	"""
	class Function(BaseExtensionKey):
		enabled=True
		name="Function"

		def callback(extension,parent,scope):
			...




	"""
		Description: Declares a label
		Parameters: name:str[required]
	"""
	class Label(BaseExtensionKey):
		enabled=True
		name="Label"

		def callback(extension,parent,scope):
			...





	"""
		Description: Calls a function
		Parameters: name:str[required]
	"""
	class Call(BaseExtensionKey):
		enabled=True
		name="Call"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Looping ~~~~~~~~~~~
	"""
		Description: Loops until the condition is false
		Parameters: condition:str[required]
	"""
	class While(BaseExtensionKey):
		enabled=True
		name="While"

		def callback(extension,parent,scope):
			...





	"""
		Description: Iterates through each item in a list 
		Parameters: arr:list[required]
	"""
	class Foreach(BaseExtensionKey):
		enabled=True
		name="Foreach"

		def callback(extension,parent,scope):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

