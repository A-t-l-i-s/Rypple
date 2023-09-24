import sys
import os
from pathlib import Path

from Rypple import *





if (__name__ == "__main__"):
	path = Path("manifest.ryp")



	if (path.exists() and path.is_file()):
		# Create scope
		scope = Rypple_Scope()
		scope.exceptionLevel = 0

		# Read file
		base = Rypple.readFile("manifest.ryp")

		# Set debug
		scope.constants.dev.debug = True

		# Compile file
		scope.run(base)
		scope.wait()


	else:
		print("Couldn't find manifest")





