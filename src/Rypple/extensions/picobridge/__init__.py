from RFTLib.Core.Exception import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Decorators.Label import *

from ...extension import *






@RFT_Name("PicoBridge")
@RFT_Description("")
@RFT_Enabled(True)
class Extension(Rypple_Extension):
	def init(cls, scope):
		from PicoBridge import PicoBridge

		scope.variables.picobridge = PicoBridge(None)





	@RFT_Name("Bridge")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Bridge(cls, step, scope, namespace):
		# PicoBridge namespace
		picobridge = scope.variables.picobridge



		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				# If port open then close
				if (picobridge.serial.is_open):
					picobridge.serial.close()

				# Change port
				picobridge.serial.port = value

				try:
					# Try to open serial port
					picobridge.serial.open()
				except:
					...
			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Pull")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Pull(cls, step, scope, namespace):
		# PicoBridge namespace
		picobridge = scope.variables.picobridge



		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				# If port open then close
				if (picobridge.serial.is_open):
					picobridge.pull(value)
			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Push")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Push(cls, step, scope, namespace):
		# PicoBridge namespace
		picobridge = scope.variables.picobridge



		if (step.value != None):
			value = scope.evaluate(
				step.value,
				namespace = namespace
			)


			if (isinstance(value, str)):
				# If port open then close
				if (picobridge.serial.is_open):
					picobridge.push(value)

			else:
				return RFT_Exception.TypeError(
					type(value)
				) # Invalid Type
		else:
			return RFT_Exception.NoValue() # No Value





	@RFT_Name("Reboot")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Reboot(cls, step, scope, namespace):
		# PicoBridge namespace
		picobridge = scope.variables.picobridge


		if (step.value == None):
			if (picobridge.serial.is_open):
				picobridge.reboot()

		else:
			return RFT_Exception.NoValue() # Has Value





	@RFT_Name("Console")
	@RFT_Description("")
	@RFT_Enabled(True)
	def Console(cls, step, scope, namespace):
		# PicoBridge namespace
		picobridge = scope.variables.picobridge


		if (step.value == None):
			if (picobridge.serial.is_open):
				picobridge.console()

		else:
			return RFT_Exception.NoValue() # Has Value








