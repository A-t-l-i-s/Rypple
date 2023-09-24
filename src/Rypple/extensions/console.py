import sys

from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ..extension import *






@RFT_Name("Console")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		...





	@RFT_Name("Print")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Print(cls, step, scope, namespace):
		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)

			print(
				str(value)
			)
		else:
			print()




