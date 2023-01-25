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



	def init(cls,scope):
		...





	"""
		Description: ...
		Parameters: ...
	"""
	class If(Rypple_ExtensionKey):
		name = "If"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (value):
					scope.run(step,namespace)

				else:
					i=step.getIndex(key=cls.Else.name)

					if (i > -1):
						scope.run(step.steps[i],namespace)

			else:
				return Unknown()





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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (scope.validVar(value)):
					step.temp = True

					namespace[value] = step


				else:
					return Unknown()
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)

				if (isinstance(value,Rypple_Step)):
					if (value.key == cls.Function.name):
						scope.run(value,namespace)


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
	class Thread(Rypple_ExtensionKey):
		name = "Thread"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				thread = threading.Thread(
					target=cls.Call.callback,
					args=(cls,step,scope,namespace),
					kwargs={},
					daemon=True
				)

				thread.start()


			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class For(Rypple_ExtensionKey):
		name = "For"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (isinstance(value,str)):
					i = value.find(':')
					if (i > -1):
						name = value[:i].strip()
						val = value[i + 1:].strip()

						newValue = scope.evaluate(val,namespace)

						if (isinstance(newValue,Iterable)):
							for c in newValue:
								namespace[name] = c

								scope.run(step,namespace)


							namespace.pop(value)


						else:
							return Unknown()
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				while (value):
					scope.run(step,namespace)

					value = scope.evaluate(step.value,namespace)


			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Namespace(Rypple_ExtensionKey):
		name = "Namespace"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)



				# Check if value is temp
				isTemp = False

				if (isinstance(var,str)):
					if (len(var) > 0):
						if (var[0] == '~'):
							isTemp = True



				if (scope.validVar(value)):
					# Create namespace
					v = Rypple_Namespace(temp=isTemp)


					# Assign namespace
					namespace[value] = v


					# Run scope
					scope.run(step,v)

				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Join(Rypple_ExtensionKey):
		name = "Join"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (isinstance(value,Rypple_Namespace)):
					for k,v in value.values().items():
						namespace[k] = v


				elif (isinstance(value,dict)):
					for k,v in value.items():
						namespace[k] = v


				else:
					return Unknown()
			else:
				return Unknown()





	"""
		Description: ...
		Parameters: ...
	"""
	class Inc(Rypple_ExtensionKey):
		name = "Inc"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (scop.validVar(value)):
					if (namespace.contains(value)):
						try:
							namespace[value] += 1

						except:
							return Unknown()


					elif (scope.variables.contains(value)):
						try:
							scope.variables[value] += 1

						except:
							return Unknown()
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
	class Dec(Rypple_ExtensionKey):
		name = "Dec"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (scop.validVar(value)):
					if (namespace.contains(value)):
						try:
							namespace[value] -= 1

						except:
							return Unknown()


					elif (scope.variables.contains(value)):
						try:
							scope.variables[value] -= 1

						except:
							return Unknown()
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (isinstance(value,str)):
					try:
						mod = importlib.import_module(value)

						scope.modules[value] = mod

					except:
						return Unknown()
				else:
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (isinstance(value,str)):
					if (scope.loadExtension(value)):
						...
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


				if (isinstance(value,str)):
					if (scope.validVar(value)):
						if (namespace.contains(value)):
							namespace.pop(value)


						elif (scope.variables.contains(value)):
							scope.variables.pop(value)


						else:
							return Unknown()
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
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)


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
			if (not step.isCmd()):
				if (not scope.constants.exit):
					scope.constants.exit = True


				else:
					return Unknown()
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








