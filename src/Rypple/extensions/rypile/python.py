from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ...extension import *






@RFT_Name("RyPile-Python")
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
		rypile.exe = "py"





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


			if (isinstance(value, (str, float, int))):
				rypile.args.append(f"-{value}")

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("DontWriteBytecode")
	@RFT_Description("")
	@RFT_Enabled(True)
	def DontWriteBytecode(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-B"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.args.append(cmd)





	@RFT_Name("Unbuffered")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Unbuffered(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-u"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.args.append(cmd)





	@RFT_Name("Debug")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Debug(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		# Command
		cmd = "-d"


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				if (value):
					rypile.args.append(cmd)

				else:
					rypile.args.remove(cmd)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Option")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Option(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args += "-X", value

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Compile")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Compile(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.args += "-c", value

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





