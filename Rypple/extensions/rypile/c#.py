from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile.C#")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "csc"

		rypile.args.append("/nologo")








	@Name("File")
	@Description("")
	@Enabled(True)
	def File(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(value)

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Out")
	@Description("")
	@Enabled(True)
	def Out(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"/out:{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Reference")
	@Description("")
	@Enabled(True)
	def Reference(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"/reference:{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value




