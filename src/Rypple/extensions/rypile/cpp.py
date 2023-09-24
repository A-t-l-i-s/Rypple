from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ...extension import *






@RFT_Name("RyPile-C++")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")
		scope.loadExtension("RyPile-C")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "g++"




