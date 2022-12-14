from ..extension import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "Console"
	enabled = True





	"""
		Description: ...
		Parameters: ...
	"""
	class Print(Rypple_ExtensionKey):
		name = "Print"
		enabled = True


		def callback(cls,step,scope):
			value = scope.evaluate(step.value)
			
			print(value)





