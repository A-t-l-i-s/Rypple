from ..extension import *
from ..namespace import *
from ..exceptions import *
from ..decorators import *





__all__=["Extension"]





@Name("C")
@Description("C compiler for RyPile")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		scope.loadExtension("RyPile")


		# Set loaded extension
		scope.variables.rypile.ext = cls


		# Set args
		scope.variables.rypile.args.clear()
		scope.variables.rypile.exe = "gcc"





	@Name("File")
	@Description("Adds input file")
	@Parameters(path = str)
	@Enabled(True)
	class File(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(value)

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Bit")
	@Description("Sets architecture mode")
	@Parameters(bit = int)
	@Enabled(True)
	class Bit(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,int)):
					scope.variables.rypile.args.append(f"-m{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Out")
	@Description("Sets output file")
	@Parameters(path = str)
	@Enabled(True)
	class Out(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(f"-o{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Optimize")
	@Description("Sets optimization level")
	@Parameters(level = int)
	@Enabled(True)
	class Optimize(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,int)):
					scope.variables.rypile.args.append(f"-O{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Version")
	@Description("Sets compilation version")
	@Parameters(ver = str)
	@Enabled(True)
	class Version(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(f"--std={value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("IncludePath")
	@Description("Add search path for includes")
	@Parameters(path = str)
	@Enabled(True)
	class IncludePath(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(f"-I{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("LibraryPath")
	@Description("Adds search path for libraries")
	@Parameters(path = str)
	@Enabled(True)
	class LibraryPath(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(f"-L{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Library")
	@Description("Includes a library")
	@Parameters(name = str)
	@Enabled(True)
	class Library(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,str)):
					scope.variables.rypile.args.append(f"-l{value}")

				else:
					return Unknown()
			else:
				return Unknown()





	@Name("Shared")
	@Description("Sets shared mode")
	@Parameters(enabled = bool)
	@Enabled(True)
	@Value("cmd","-shared")
	class Shared(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,bool)):
					if (value):
						scope.variables.rypile.args.append(cls.cmd)

					else:
						scope.variables.rypile.args.remove(cls.cmd)
				else:
					return Unknown()
			else:
				scope.variables.rypile.args.append(cls.cmd)





	@Name("Static")
	@Description("Sets static mode")
	@Parameters(enabled = bool)
	@Enabled(True)
	@Value("cmd","-static")
	class Static(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,bool)):
					if (value):
						scope.variables.rypile.args.append(cls.cmd)

					else:
						scope.variables.rypile.args.append(cls.cmd)

				else:
					return Unknown()
			else:
				scope.variables.rypile.args.append(cls.cmd)





	@Name("Window")
	@Description("Sets if console is hidden")
	@Parameters(enabled = str)
	@Enabled(True)
	@Value("cmd","-Wl,-subsystem,windows")
	class Window(Rypple_ExtensionKey):
		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				if (isinstance(value,bool)):
					if (value):
						scope.variables.rypile.args.append(cls.cmd)

					else:
						scope.variables.rypile.args.append(cls.cmd)

				else:
					return Unknown()
			else:
				scope.variables.rypile.args.append(cls.cmd)









