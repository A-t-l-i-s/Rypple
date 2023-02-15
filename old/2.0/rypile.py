import sys
import ntpath

from pathlib import Path

from Rypple import *





if (__name__ == "__main__"):
	rypple = Rypple()
	scope = Rypple_Scope()

	scope.loadExtension("RyPile")
	scope.loadExtension("Python")



	for f in sys.argv:
		if (ntpath.exists(f) and ntpath.isfile(f)):
			groups = rypple.parseFile(f)

			scope.constants.file.path = Path(f).resolve()

			scope.run(groups)



