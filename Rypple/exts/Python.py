from ..extension import *
from ..namespace import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "Python"
	enabled = True



	def init(cls,scope):
		scope.loadExtension("RyPile")





	"""
		Description: ...
		Parameters: ...
	"""
	class Python(Rypple_ExtensionKey):
		name = "Python"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (not step.isCmd()):
				scope.variables.rypile.args.clear()

				scope.variables.rypile.exe = "python"

			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class PyFile(Rypple_ExtensionKey):
		name = "PyFile"
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




