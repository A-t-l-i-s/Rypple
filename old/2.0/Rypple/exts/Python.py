from ..extension import *
from ..namespace import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "Python"
	enabled = True



	def init(cls,scope):
		scope.loadExtension("RyPile")


		# Set loaded extension
		scope.variables.rypile.ext = cls


		# Set args
		scope.variables.rypile.args.clear()
		scope.variables.rypile.exe = "python"





	"""
		Description: ...
		Parameters: ...
	"""
	class File(Rypple_ExtensionKey):
		name = "File"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(value)

				else:
					return Unknown()
			else:
				return Unknown()




