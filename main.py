from Rypple import *
import re, json, time






if (__name__ == "__main__"):
	r=Rypple()


	groups=r.parseFile("tests/dummy.ryp")


	scope=Rypple_Scope()
	scope.run(groups)


	print(json.dumps(scope.variables.toJSON(),indent=4))





