import time
import importlib
import traceback

from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ..extension import *






@RFT_Name("Core")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		...





	@RFT_Name("Import")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Import(cls, step, scope, namespace):
		if (step.value != None):
			try:
				# Import module
				module = importlib.import_module(
					step.value
				)

				# Add module to scope modules
				scope.modules[
					step.value
				] = module

			except:
				return RFT_Exception(
					f"Error importing '{value}'",
					RFT_Exception.ERROR
				) # Failed Importing
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Extension")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Extension(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = step.value.strip()


			# If extension exists
			if (scope.extensions.contains(value)):
				# Get extension
				ext = scope.extensions[value]

				# If extension not already loaded
				if (not scope.loadedExtensions.contains(value)):
					scope.loadExtension(
						value
					)

				else:
					return RFT_Exception(
						f"'{value}' is already loaded",
						RFT_Exception.WARNING
					) # Already Loaded
			else:
				return RFT_Exception(
					f"'{value}' not found",
					RFT_Exception.WARNING
				) # Not Found
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Exit")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Exit(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)
			
			if (isinstance(value, int)): # Is Integer
				# Set exit code to value
				scope.constants.dev.exit = value


			else:
				raise RFT_Exception.TypeError(
					type(value)
				)
		else:
			# Set exit code to 1
			scope.constants.dev.exit = 1





	@RFT_Name("Function")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Function(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			# Wrap into callable function
			def wrapper():
				scope.run(
					step,
					RFT_Structure({})
				)


			scope.setVar(
				step.value,
				wrapper,
				namespace
			)

		else:
			# No function name
			raise RFT_Exception(
				"No function name present",
				RFT_Exception.ERROR
			)





	@RFT_Name("Delete")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Delete(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			if (namespace.contains(step.value)): # Contains variable
				# Remove value
				namespace.pop(step.value)

			else:
				return RFT_Exception(
					f"'{step.value}' not found",
					RFT_Exception.WARNING
				) # Not Found
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("If")
	@RFT_Description("")
	@RFT_Enabled(True)
	def If(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)
			

			if (value):
				# Run If step
				scope.run(
					step,
					namespace = namespace
				)


			else:
				found = False
				# Look for Else statement in children
				for s in step.children:
					if (s.key == cls.Else.name):
						if (found):
							return RFT_Exception(
								"Multiple else statements detected",
								RFT_Exception.WARNING
							)

						else:
							# Found Else steo
							found = True

							# Run Else step
							scope.run(
								s,
								namespace = namespace
							)


		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Else")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Else(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			return RFT_Exception.HasValue(1)





	@RFT_Name("For")
	@RFT_Description("")
	@RFT_Enabled(True)
	def For(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)

			try:
				for i in value:
					namespace[
						scope.constants.dev.loopVar
					] = i

					if (not scope.run(
						step,
						namespace = namespace
					)):
						break

			except:
				return RFT_Exception(
					traceback.format_exc(),
					RFT_Exception.ERROR
				)


		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("While")
	@RFT_Description("")
	@RFT_Enabled(True)
	def While(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			try:
				while (value := scope.evaluate(
						step.value,
						namespace = namespace
					)):

					if (not scope.run(
						step,
						namespace = namespace
					)):
						break

			except:
				return RFT_Exception(
					traceback.format_exc(),
					RFT_Exception.ERROR
				)


		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Break")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Break(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			return RFT_Exception.HasValue() # Has Value

		else:
			# Break loop
			scope.constants.dev.breakScope = True





	@RFT_Name("Join")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Join(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, dict)):
				value = RFT_Structure(value)


			if (isinstance(value, RFT_Structure)):
				for k in value.keys():
					namespace[k] = value[k]


			else:
				return RFT_Exception.TypeError(type(value)) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Incr")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Incr(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (hasattr(value, "__add__")):
				namespace[step.value] = value.__add__(1)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Decr")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Decr(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (hasattr(value, "__sub__")):
				namespace[step.value] = value.__sub__(1)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Delay")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Delay(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			value = step.value # Get Value


			deltas = (
				("ns", 1 / 1000 / 1000),
				("ms", 1 / 1000),
				("s", 1),
				("m", 60),
				("h", 60 * 60),
				("d", 60 * 60 * 24),
			)


			# Default vars
			delta = None


			# Find current delta
			for d in deltas:
				if (value.endswith(d[0])):
					delta = d
					break


			if (delta != None):
				# Length of delta
				l = len(delta[0])


				# Remove delta
				v = value[:-l]


				# Convert to float
				try:
					newVal = float(v)
				except:
					newVal = None


				# Value is not
				if (newVal != None):
					# Value to seconds
					secs = newVal * delta[1]

					# Delay program
					time.sleep(secs)

				else:
					return RFT_Exception(
						"Invalid time value",
						RFT_Exception.ERROR
					) # Invalid Value
			else:
				return RFT_Exception(
					"Invalid time delta",
					RFT_Exception.ERROR
				) # Invalid Delta
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Var")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Var(cls, step, scope, namespace):
		if (step.value != None): # Value Present
			scope.constants.dev.loopVar = step.value

		else:
			# No function name
			raise RFT_Exception(
				"No function name present",
				RFT_Exception.ERROR
			)







