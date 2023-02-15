import importlib

from Rypple.__init__ import *
from Rypple.extension import *
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
		value = scope.evaluate(step.value,namespace = namespace)


		if (step.hasValue()):
			if (isinstance(value,str)):
				try:
					# Import module
					module = importlib.import_module(value)

					# Add module to scope modules
					scope.modules[value] = module

				except:
					return Rypple_Error(f"Error importing '{value}'") # Failed Importing
			else:
				return Rypple_Error(f"Invalid type '{type(value).__name__}'") # Invalid Type
		else:
			return Rypple_Error(f"Requires value") # No Value








	@Name("Include")
	@Description("")
	@Enabled(True)
	def Include(cls,step,scope,namespace):
		return Rypple_Warning()








	@Name("Extension")
	@Description("")
	@Enabled(True)
	def Extension(cls,step,scope,namespace):
		value = scope.evaluate(step.value,namespace = namespace)


		if (step.hasValue()): # Value Present
			if (isinstance(value,str)): # Is String
				value = value.strip()


				if (Rypple.validVar(value)):
					# Get extension
					ext = scope.extensions.get(value)


					# If extension exists
					if (ext != None):

						# If extension not already loaded
						if (ext not in scope.loadedExtensions):

							# Initialize extension
							ext.init(ext,scope)

							# Add extension
							scope.loadedExtensions[value] = ext


							return Rypple_Log(f"Succssfully loaded '{value}'") # Success
						else:
							return Rypple_Warning(f"'{value}' is already loaded") # Already Loaded
					else:
						return Rypple_Warning(f"'{value}' not found") # Not Found
				else:
					return Rypple_Error(f"Invalid var '{value}'") # Invalid Variable
			else:
				return Rypple_Error(f"Invalid type '{type(value).__name__}'") # Invalid Type
		else:
			return Rypple_Error(f"Requires value") # No Value







	@Name("RemoveExtension")
	@Description("")
	@Enabled(True)
	def RemoveExtension(cls,step,scope,namespace):
		value = scope.evaluate(step.value,namespace = namespace)


		if (step.hasValue()): # Value Present
			if (isinstance(value,str)): # Is String
				value = value.strip()


				# Check variable validation
				if (Rypple.validVar(value)):

					# If extension already loaded
					if (value in scope.loadedExtensions):
						# Remove extension
						scope.loadedExtensions.pop(value)


						return Rypple_Log(f"Succssfully removed '{value}'") # Success
					else:
						return Rypple_Warning(f"'{value}' isn't loaded") # Already Loaded
				else:
					return Rypple_Error(f"Invalid var '{value}'") # Invalid Variable
			else:
				return Rypple_Error(f"Invalid type '{type(value).__name__}'") # Invalid Type
		else:
			return Rypple_Error(f"Requires value") # No Value








	@Name("Exit")
	@Description("")
	@Enabled(True)
	def Exit(cls,step,scope,namespace):
		value = scope.evaluate(step.value,namespace = namespace)


		if (step.hasValue()): # Value Present
			if (isinstance(value,int)): # Is Integer
				# Set exit code to value
				scope.constants.exit = value

				return Rypple_Log(f"Exiting with exit code '{value}'") # Success
			else:
				return Rypple_Critical(f"Invalid type '{type(value).__name__}'") # Invalid Type
		

		else:
			# Set exit code to default 1
			scope.constants.exit = 1
			
			return Rypple_Log(f"Exiting with exit code '1'") # Success





