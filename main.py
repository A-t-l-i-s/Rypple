import re
import time

from Rypple import *
from Rypple.scope import *





if (__name__ == "__main__"):
	base = Rypple.readFile("./tests/dummy.ryp")
	scope = Rypple_Scope()
	scope.constants.debug = True
	

	scope.run(base)
	scope.wait()


	# base.print()
	# scope.variables.resolve()
	# scope.variables.printList()


	# base.toFile("./tests/dummy.ryc")



