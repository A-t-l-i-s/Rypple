from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile.C")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "gcc"








	@Name("File")
	@Description("")
	@Enabled(True)
	def File(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(value)
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Bit")
	@Description("")
	@Enabled(True)
	def Bit(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,int)):
				rypile.args.append(f"-m{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("IncludePath")
	@Description("")
	@Enabled(True)
	def IncludePath(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"-I{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("LibraryPath")
	@Description("")
	@Enabled(True)
	def LibraryPath(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"-L{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Library")
	@Description("")
	@Enabled(True)
	def Library(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"-l{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Version")
	@Description("")
	@Enabled(True)
	def Version(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"--std={value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Shared")
	@Description("")
	@Enabled(True)
	def Shared(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-shared"


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			rypile.args.append(cmd)








	@Name("Compression")
	@Description("")
	@Enabled(True)
	def Compression(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,int)):
				rypile.args.append(f"-O{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("NoConsole")
	@Description("")
	@Enabled(True)
	def NoConsole(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-Wl,-subsystem,windows"


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			rypile.args.append(cmd)








	@Name("Static")
	@Description("")
	@Enabled(True)
	def Static(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-static"


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			rypile.args.append(cmd)








	@Name("Out")
	@Description("")
	@Enabled(True)
	def Out(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args.append(f"-o{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value




