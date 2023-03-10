from pathlib import Path

from Rypple.__init__ import *
from Rypple.step import *
from Rypple.extension import *
from Rypple.namespace import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("FileSystem")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		...








	@Name("Rename")
	@Description("")
	@Enabled(True)
	def Rename(cls,step,scope,namespace):
		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (isinstance(value,(list,tuple))):
				if (len(value) == 2):
					f1,f2 = value


					if (isinstance(f1,str) and isinstance(f2,str)):
						f1 = Path(f1)
						f2 = Path(f2)

						if (f1.exists()):
							f1.rename(f2)

						else:
							return Rypple_Error("File doesn't exist") # File not exist
					else:
						return Rypple_Error("Path not string") # Invalid path type
				else:
					return Rypple_Error("List must have length of 2")
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value





