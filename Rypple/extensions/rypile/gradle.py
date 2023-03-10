from Rypple import *
from Rypple.extension import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile.Gradle")
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
		rypile.exe = "gradlew.bat"








	@Name("Build")
	@Description("")
	@Enabled(True)
	def Build(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile

		cmd = "build"


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


		rypl = scope.loadedExtensions["RyPile"]
		
		return rypl.Done(
			rypl,
			Rypple_Step(
				value = None
			),
			scope,
			namespace
		)










