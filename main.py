from Rypple import *

from RFTLib.Core.Structure import *
from RFTLib.Core.Buffer import *





if (__name__ == "__main__"):
	scope = Rypple_Scope()



	base = Rypple.readFile("tests/dummy.ryp")

	scope.exceptionLevel = 0
	scope.run(base)
	scope.wait()





