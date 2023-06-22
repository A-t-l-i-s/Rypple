import time

from RFTLib.Core.Decorators.Label import *

from ..extension import *






@RFT_Name("Core")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		...





	@RFT_Name("Test")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Test(cls, step, scope, namespace):
		print(scope.variables.keys())





	@RFT_Name("Exit")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Exit(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)
			
			if (isinstance(value, int)): # Is Integer
				# Set exit code to value
				scope.constants.dev.exit = value

		else:
			# Set exit code to 1
			scope.constants.dev.exit = 1





