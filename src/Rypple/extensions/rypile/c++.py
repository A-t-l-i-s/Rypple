from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile.C++")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")
		scope.loadExtension("RyPile.C")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "g++"






