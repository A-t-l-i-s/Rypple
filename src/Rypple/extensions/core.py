import time
import importlib
from typing import Iterable

from Rypple.__init__ import *
from Rypple.step import *
from Rypple.extension import *
from Rypple.namespace import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("Core")
@Description("")
@Enabled(True)
@Value("core",True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		...








	@Name("Import")
	@Description("")
	@Enabled(True)
	def Import(cls,step,scope,namespace):
		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (isinstance(value,str)):
				try:
					# Import module
					module = importlib.import_module(value)

					# Add module to scope modules
					scope.modules[value] = module


					return Rypple_Log(f"Succssfully imported '{value}'") # Success
				except:
					return Rypple_Error(f"Error importing '{value}'") # Failed Importing
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Include")
	@Description("")
	@Enabled(True)
	def Include(cls,step,scope,namespace):
		return Rypple_Warning()








	@Name("Extension")
	@Description("")
	@Enabled(True)
	def Extension(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)
	

			if (isinstance(value,str)): # Is String
				value = value.strip()


				# Get extension
				ext = scope.extensions.get(value)


				# If extension exists
				if (ext != None):

					# If extension not already loaded
					if (ext not in scope.loadedExtensions):

						# Load extension
						scope.loadExtension(ext)


						return Rypple_Log(f"Succssfully loaded '{value}'") # Success
					else:
						return Rypple_Warning(f"'{value}' is already loaded") # Already Loaded
				else:
					return Rypple_Warning(f"'{value}' not found") # Not Found
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Exit")
	@Description("")
	@Enabled(True)
	def Exit(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (isinstance(value,int)): # Is Integer

				# Set exit code to value
				scope.constants.exit = value


				return Rypple_Log(f"Exiting with exit code '{value}'") # Success
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		

		else:
			# Set exit code to 1
			scope.constants.exit = 1
			
			return Rypple_Log(f"Exiting with exit code '1'") # Success








	@Name("Delete")
	@Description("")
	@Enabled(True)
	def Delete(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = step.value
		

			if (namespace.contains(value)): # Contains variable

				# Remove value
				namespace.pop(value)


				return Rypple_Log(f"Succssfully deleted '{value}'") # Success
			else:
				return Rypple_Error(f"'{value}' not found") # Not Found
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Function")
	@Description("")
	@Enabled(True)
	def Function(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = step.value
			

			if (Rypple.validVar(value)): # Variable validation

				# Set variable
				scope.setVar(
					value,
					step,
					namespace = namespace
				)


				return Rypple_Log(f"Succssfully created function '{value}'") # Success
			else:
				return Rypple_Error(f"Invalid var '{value}'") # Invalid Variable
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Call")
	@Description("")
	@Enabled(True)
	def Call(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (isinstance(value,Rypple_Step)): # Is Rypple_Step
				# Call function
				if (scope.run(value,namespace = namespace)):
					return Rypple_Log(f"Succssfully called '{value.value}'") # Success

				else:
					return Rypple_Error(f"'{value.value}' failed to run") # Failed
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("If")
	@Description("")
	@Enabled(True)
	def If(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (value):
				# Call scope
				if (scope.run(step,namespace = namespace)):
					return Rypple_Log("If condition passed") # Success

				else:
					return Rypple_Log("If condition failed") # Failed


			else:
				for s in step.children:
					if (s.key == cls.Else.name):
						if (scope.run(s,namespace = namespace)):
							return Rypple_Log("Else statement passed") # Success

						else:
							return Rypple_Log("Else statement failed") # Failed


				return Rypple_Log("No if statement")
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Else")
	@Description("")
	@Enabled(True)
	def Else(cls,step,scope,namespace):
		if (not step.hasValue()): # No Value Present
			return Rypple_Log("Ignoring else statement") # Success
		else:
			return Rypple_Exception.HasValue() # Can't Accept Value








	@Name("For")
	@Description("")
	@Enabled(True)
	def For(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)
			

			if (isinstance(value,Iterable)):
				# Iterate through value
				for i in value:
					# Set loop variable
					namespace[Rypple.loopVar] = i

					# Call scope
					if (not scope.run(step,namespace = namespace)):
						return Rypple_Log("Breaking loop")



				# Remove var
				namespace.pop(Rypple.loopVar)


				return Rypple_Log("Succssfully ran for loop") # Success
			else:
				return Rypple_Error("Value not iterable") # Not iterable
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("While")
	@Description("")
	@Enabled(True)
	def While(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			while (scope.evaluate(step.value,namespace = namespace)):
				# Call scope
				if (not scope.run(step)):
					return Rypple_Log("Breaking loop")


			return Rypple_Log("Succssfully ran while loop") # Success
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Break")
	@Description("")
	@Enabled(True)
	def Break(cls,step,scope,namespace):
		...








	@Name("Join")
	@Description("")
	@Enabled(True)
	def Join(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,dict)):
				value = Rypple_Namespace(value)


			if (isinstance(value,Rypple_Namespace)):
				for k in value.keys():
					if (k != "__temp__"):
						namespace[k] = value[k]


				return Rypple_Log("Succssfully joined namespace") # Success
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Incr")
	@Description("")
	@Enabled(True)
	def Incr(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			if (namespace.contains(step.value)): # Variable in namespace
				# Get key as string
				key = step.value

				# Evaluate value
				value = scope.evaluate(key,namespace = namespace)


				if (isinstance(value,(int,float))):
					# Increment value
					value += 1

					# Set value
					scope.setVar(
						key,
						value,
						namespace = namespace
					)

				else:
					return Rypple_Exception.TypeError(type(value)) # Invalid Type
			else:
				return Rypple_Error("Variable doesn't exist") # Variable doesn't exist
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Decr")
	@Description("")
	@Enabled(True)
	def Decr(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			if (namespace.contains(step.value)): # Variable in namespace
				# Get key as string
				key = step.value

				# Evaluate value
				value = scope.evaluate(key,namespace = namespace)



				if (isinstance(value,(int,float))):
					# Decrement value
					value -= 1

					# Set value
					scope.setVar(
						key,
						value,
						namespace = namespace
					)

				else:
					return Rypple_Exception.TypeError(type(value)) # Invalid Type
			else:
				return Rypple_Error("Variable doesn't exist") # Variable doesn't exist
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Delay")
	@Description("")
	@Enabled(True)
	def Delay(cls,step,scope,namespace):
		if (step.hasValue()): # Value Present
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,(int,float))):
				# Delay program
				time.sleep(value)


			elif (isinstance(value,str)):
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
						return Rypple_Error("Invalid time value") # Invalid Value
				else:
					return Rypple_Error("Invalid time delta") # Invalid Delta
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value





