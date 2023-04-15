from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile.Python")
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
		rypile.exe = "py"








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








	@Name("Version")
	@Description("")
	@Enabled(True)
	def Version(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,(str,float,int))):
				rypile.args.append(f"-{value}")

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("DontWriteBytecode")
	@Description("")
	@Enabled(True)
	def DontWriteBytecode(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-B"


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








	@Name("Debug")
	@Description("")
	@Enabled(True)
	def Debug(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-d"


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








	@Name("Unbuffered")
	@Description("")
	@Enabled(True)
	def Unbuffered(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "-u"


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








	@Name("Option")
	@Description("")
	@Enabled(True)
	def Option(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args += "-X", value

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Compile")
	@Description("")
	@Enabled(True)
	def Compile(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.args += "-c", value

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value





