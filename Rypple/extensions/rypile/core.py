import os
import subprocess
from pathlib import Path
from typing import Iterable

from Rypple import *
from Rypple.extension import *
from Rypple.namespace import *
from Rypple.decorators import *
from Rypple.exceptions import *





__all__ = ("Extension",)





@Name("RyPile")
@Description("")
@Enabled(True)
class Extension(Rypple_Extension):
	def init(cls,scope):
		scope.variables.rypile = Rypple_Namespace({
			"popout": False,
			"args": [],
			"exe": None,
			"env": dict(os.environ),
			"ext": None,

			"changePath": None,
			"originalPath": os.getcwd(),

			"processes": [],

			"__temp__": True
		})








	@Name("Run")
	@Description("")
	@Enabled(True)
	def Run(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)
			

			# If string convert to a single item tuple
			if (isinstance(value,str)):
				value = (value,)


			# If value is iterable
			if (isinstance(value,Iterable)):
				args = []

				# Convert values to string
				for a in value:
					args.append(str(a))



				# If true then popout console into new window
				if (rypile.popout):
					creationFlags = subprocess.CREATE_NEW_CONSOLE

				else:
					creationFlags = 0x00


				try:
					# Create new subprocess attached to main process
					process = subprocess.Popen(
						args,
						creationflags = creationFlags,
						env = rypile.env
					)

					rypile.processes.append(process)


					return Rypple_Log(f"Succssfully started process '{process.pid}'") # Success
				except:
					return Rypple_Error("Process failed to start") # Process Failed
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Extra")
	@Description("")
	@Enabled(True)
	def Extra(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)
			

			# If string convert to a single item tuple
			if (isinstance(value,str)):
				value = (value,)


			# If value is iterable
			if (isinstance(value,Iterable)):
				# Convert value to tuple
				val = tuple(value)

				# Add args to rypile ags
				rypile.args += val


				return Rypple_Log("Succssfully added extra args to rypile args") # Success
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Reset")
	@Description("")
	@Enabled(True)
	def Reset(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (not step.hasValue()):
			# Reset args
			rypile.args.clear()

			# Remove extension from current rypile extension
			rypile.ext = None


			return Rypple_Log("Succssfully reset rypile") # Success
		else:
			return Rypple_Exception.HasValue() # Has Value








	@Name("Directory")
	@Description("")
	@Enabled(True)
	def Directory(cls,step,scope,namespace):
		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,(str,os.PathLike))):
				# Convert to pathlike
				path = Path(value)


				if (path.is_dir()):
					# Change current directory
					os.chdir(path)


					return Rypple_Log(f"Succssfully changed directory to '{path}'")
				else:
					return Rypple_Log("Path is not a directory")
			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value








	@Name("Done")
	@Description("")
	@Enabled(True)
	def Done(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile
		

		if (not step.hasValue()):
			# If extension as loaded
			if (rypile.ext in scope.loadedExtensions):
				# Remove extension from loaded
				scope.loadedExtensions.remove(rypile.ext)



			# Create compilation args
			args = []

			if (isinstance(rypile.exe,str)):
				args.append(rypile.exe)


			args += rypile.args


			# Compile args
			yield cls.Run(
				cls,
				Rypple_Step(
					value = args
				),
				scope,
				namespace
			)


			# Wait for process
			yield cls.Wait(
				cls,
				Rypple_Step(
					value = None
				),
				scope,
				namespace
			)


			# Reset rypile
			yield cls.Reset(
				cls,
				Rypple_Step(
					value = None
				),
				scope,
				namespace
			)


			# Reset directory
			yield cls.Directory(
				cls,
				Rypple_Step(
					value = scope.variables.rypile.originalPath
				),
				scope,
				namespace
			)

		else:
			return Rypple_Exception.HasValue() # Has Value








	@Name("Popout")
	@Description("")
	@Enabled(True)
	def Popout(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile
		

		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,bool)):
				rypile.popout = value

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			rypile.popout = True








	@Name("Wait")
	@Description("")
	@Enabled(True)
	def Wait(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile
		

		if (not step.hasValue()):
			for p in rypile.processes:
				p.wait()

			rypile.processes.clear()

		else:
			return Rypple_Exception.HasValue()








	@Name("Executable")
	@Description("")
	@Enabled(True)
	def Executable(cls,step,scope,namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.hasValue()):
			value = scope.evaluate(step.value,namespace = namespace)


			if (isinstance(value,str)):
				rypile.exe = value

			else:
				return Rypple_Exception.TypeError(type(value)) # Invalid Type
		else:
			return Rypple_Exception.NoValue() # No Value




