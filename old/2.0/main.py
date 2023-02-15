from Rypple import *
import re, json, time






if (__name__ == "__main__"):
	scope = load("tests/dummy.ryp")

	print(json.dumps(scope.toJSON(),indent=4,cls=Rypple_JSON_Encoder))




