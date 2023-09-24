from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ...extension import *






@RFT_Name("RyPile-Javascript")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "node"





	@RFT_Name("File")
	@RFT_Description("")
	@RFT_Enabled(True)
	def File(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(value)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





