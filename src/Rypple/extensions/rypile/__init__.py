import os
import subprocess

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

			"changePath": None,
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








