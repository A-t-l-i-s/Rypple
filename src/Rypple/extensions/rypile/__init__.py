import os
import subprocess

from pathlib import Path

from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *


from ...extension import *






@RFT_Name("RyPile")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		scope.variables.rypile = RFT_Structure({
			"popout": False,
			"args": [],
			"exe": None,
			"env": dict(os.environ),
			"ext": None,

			"originalPath": os.getcwd(),

			"processes": [],

			"__temp__": True
		})





	@RFT_Name("Run")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Run(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)
			

			# If string convert to a single item tuple
			if (isinstance(value, str)):
				value = (value,)


			# If value is iterable
			if (isinstance(value, (tuple, list))):
				args = []

				# Convert values to string
				for a in value:
					args.append(
						str(a)
					)



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
						env = rypile.env.toDict()
					)

					rypile.processes.append(
						process
					)
				except:
					return RFT_Exception(
						"Process failed to start",
						RFT_Exception.ERROR
					) # Process Failed
			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Extra")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Extra(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)
			

			# If string convert to a single item tuple
			if (isinstance(value, str)):
				value = (value,)


			# If value is iterable
			if (isinstance(value, (tuple, list))):
				# Convert value to tuple
				val = tuple(value)

				# Add args to rypile ags
				rypile.args += val

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Reset")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Reset(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value == None):
			# Reset args
			rypile.args.clear()

			# Remove extension from current rypile extension
			rypile.ext = None

		else:
			return RFT_Exception.NoValue() # Has Value





	@RFT_Name("Directory")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Directory(cls, step, scope, namespace):
		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, (str, os.PathLike))):
				# Convert to pathlike
				path = Path(value)


				if (path.is_dir()):
					# Change current directory
					os.chdir(path)

				else:
					return RFT_Exception(
						"Path is not a directory",
						RFT_Exception.WARNING
					)
			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Popout")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Popout(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile
		

		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, bool)):
				rypile.popout = bool(value)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			rypile.popout = True





	@RFT_Name("Wait")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Wait(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value == None):
			for p in rypile.processes:
				p.wait()

			rypile.processes.clear()

		else:
			return RFT_Exception.HasValue()





	@RFT_Name("Executable")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Executable(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile


		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				rypile.exe = value

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Done")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Done(cls, step, scope, namespace):
		# Rypile namespace
		rypile = scope.variables.rypile
		

		if (step.value == None):
			# If extension as loaded
			if (scope.loadedExtensions.contains(rypile.ext)):
				# Remove extension from loaded
				scope.loadedExtensions.remove(rypile.ext)



			# Create compilation args
			args = []

			if (isinstance(rypile.exe, str)):
				args.append(rypile.exe)


			args += rypile.args


			# Compile args
			yield cls.Run(
				cls,
				RFT_Structure({
					"value": args
				}),
				scope,
				namespace
			)


			# Wait for process
			yield cls.Wait(
				cls,
				RFT_Structure({
					"value": None
				}),
				scope,
				namespace
			)


			# Reset rypile
			yield cls.Reset(
				cls,
				RFT_Structure({
					"value": None
				}),
				scope,
				namespace
			)


			# Reset directory
			yield cls.Directory(
				cls,
				RFT_Structure({
					"value": "rypile.originalPath"
				}),
				scope,
				namespace
			)

		else:
			return RFT_Exception.HasValue() # Has Value














