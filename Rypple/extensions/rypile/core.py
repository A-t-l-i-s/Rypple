from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		...