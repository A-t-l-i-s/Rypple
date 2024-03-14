from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ...extension import *






@RFT_Name("RyPile-C")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		# Load RyPile extension
		scope.loadExtension("RyPile")


		# Get rypile namespace
		rypile = scope.variables.rypile


		# Set loaded extension
		rypile.ext = cls


		# Set args
		rypile.args.clear()
		rypile.exe = "gcc"





	@RFT_Name("File")
	@RFT_Description("")
	@RFT_Enabled(True)
	def File(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(value)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Out")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Out(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(f"-o{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Bit")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Bit(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, int)):
				rypile.args.append(f"-m{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("IncludePath")
	@RFT_Description("")
	@RFT_Enabled(True)
	def IncludePath(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(f"-I{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("LibraryPath")
	@RFT_Description("")
	@RFT_Enabled(True)
	def LibraryPath(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(f"-L{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Library")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Library(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(f"-l{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Version")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Version(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args.append(f"--std={value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Shared")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Shared(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-shared"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					if (cmd in rypile.args):
						rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.args.append(cmd)





	@RFT_Name("Compression")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Compression(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, int)):
				rypile.args.append(f"-O{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("GUI")
	@RFT_Description("")
	@RFT_Enabled(True)
	def GUI(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-mwindows"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					if (cmd in rypile.args):
						rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.args.append(cmd)





	@RFT_Name("Static")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Static(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-static"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					if (cmd in rypile.args):
						rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.args.append(cmd)





