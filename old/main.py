from RyPile import *
import re
import json






if (__name__ == "__main__"):
	r=RyPile()


	steps=r.parseFile("tests/dummy")


	print(json.dumps(r.parseSteps(steps),indent=3))





