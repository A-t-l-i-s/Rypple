import sys
from RyPile import *







if (__name__=="__main__"):
	r=RyPile()

	steps=r.getSteps("test/dummy.rypl")

	scope=RyPile_Scope()
	r.run(scope,steps)


