import sys
import re
import time
import importlib
import threading
from typing import Iterable

from ..step import *
from ..extension import *
from ..namespace import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "Core"
	enabled = True





	"""
		Description: ...
		Parameters: ...
	"""
	class If(Rypple_ExtensionKey):
		name = "If"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (value):
				scope.run(step)

			else:
				i=step.getIndex(key=cls.Else.name)

				if (i > -1):
					scope.run(step.steps[i])





	"""
		Description: ...
		Parameters: ...
	"""
	class Else(Rypple_ExtensionKey):
		name = "Else"
		enabled = True


		def callback(cls,step,scope,namespace):
			return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Function(Rypple_ExtensionKey):
		name = "Function"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = step.value


			if (scope.validVar(value)):
				namespace[value] = step


			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Call(Rypple_ExtensionKey):
		name = "Call"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = step.value


			if (scope.validVar(value)):
				s = namespace[value]


				if (isinstance(s,Rypple_Step)):
					scope.run(s)


				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Thread(Rypple_ExtensionKey):
		name = "Thread"
		enabled = True


		def callback(cls,step,scope,namespace):
			thread = threading.Thread(
				target=cls.Call.callback,
				args=(cls,step,scope,namespace),
				kwargs={},
				daemon=True
			)

			thread.start()





	"""
		Description: ...
		Parameters: ...
	"""
	class For(Rypple_ExtensionKey):
		name = "For"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (isinstance(value,str)):
				i = value.find(':')
				if (i > -1):
					name=value[:i].strip()
					val=value[i + 1:].strip()

					newValue = scope.evaluate(val)

					if (isinstance(newValue,Iterable)):
						for c in newValue:
							namespace[name] = c

							scope.run(step)


						namespace.pop(value)


					else:
						return Unknown()
				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class While(Rypple_ExtensionKey):
		name = "While"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			while (newValue):
				scope.run(step)

				value = scope.evaluate(step.value)





	"""
		Description: ...
		Parameters: ...
	"""
	class Namespace(Rypple_ExtensionKey):
		name = "Namespace"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = step.value


			if (scope.validVar(value)):
				# idk wat to do here
				v = Rypple_Namespace()


				scope.run(step)

			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Include(Rypple_ExtensionKey):
		name = "Include"
		enabled = True


		def callback(cls,step,scope,namespace):
			return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Import(Rypple_ExtensionKey):
		name = "Import"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (isinstance(value,str)):
				try:
					mod = importlib.import_module(value)

					scope.modules[value] = mod

				except:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Extension(Rypple_ExtensionKey):
		name = "Extension"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (isinstance(value,str)):
				if (value in scope.extensions):
					if (value not in scope.loadedExtensions):
						ext = scope.extensions[value]

						scope.loadedExtensions[ext.name] = ext 

					else:
						return Unknown()
				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Delete(Rypple_ExtensionKey):
		name = "Delete"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (isinstance(value,str)):
				if (scope.validVar(value)):
					if (namespace.contains(value)):
						namespace.pop(value)


					else:
						return Unknown()
				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Delay(Rypple_ExtensionKey):
		name = "Delay"
		enabled = True


		def callback(cls,step,scope,namespace):
			value = scope.evaluate(step.value)


			if (isinstance(value,str)):
				# Define time deltas
				deltas=(
					("ns",1 / 1000 / 1000),
					("ms",1 / 1000),
					("s",1),
					("m",60),
					("h",60 * 60),
					("d",60 * 60 * 24),
				)


				# Default vars
				delta = None


				# Find current delta
				for d in deltas:
					if (value.endswith(d[0])):
						delta = d
						break



				if (delta != None):
					l = len(delta[0])
					v = value[:-l]

					try:
						newVal = float(v)
					except:
						newVal = None


					if (newVal != None):
						secs = newVal * delta[1]

						time.sleep(secs)

					else:
						return Unknown()
				else:
					return Unknown()



			elif (isinstance(value,(int,float))):
				time.sleep(value)



			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Exit(Rypple_ExtensionKey):
		name = "Exit"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (not scope.exit):
				scope.exit = True


			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Pass(Rypple_ExtensionKey):
		name = "Pass"
		enabled = True


		def callback(cls,step,scope,namespace):
			return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class End(Rypple_ExtensionKey):
		name = "End"
		enabled = True


		def callback(cls,step,scope,namespace):
			return Unknown()








