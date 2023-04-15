from Rypple.__init__ import *
from Rypple.step import *
from Rypple.extension import *
from Rypple.namespace import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("Console")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		...








	@Name("Print")
	@Description("")
	@Enabled(True)
	def Print(cls,step,scope,namespace):
		value = scope.evaluate(step.value,namespace = namespace)


		if (step.hasValue()):
			print(value)

		else:
			print()






