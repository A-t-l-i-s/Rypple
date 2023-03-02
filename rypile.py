import sys
import os
from pathlib import Path

from Rypple import *
from Rypple.scope import *





if (__name__ == "__main__"):
	path = Path(".")

	file = Rypple.findFile("manifest",".")



	if (file != None):
		base = Rypple.readFile(file)
		scope = Rypple_Scope()
		scope.constants.debug = True


		scope.run(base)
		scope.wait()


	else:
		print("Couldn't find manifest")





