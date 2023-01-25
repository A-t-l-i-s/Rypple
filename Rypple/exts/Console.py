import sys
import colorama

from ..extension import *
from ..namespace import *
from ..exceptions import *





__all__=["Extension"]





class Extension(Rypple_Extension):
	name = "Console"
	enabled = True



	def init(cls,scope):
		colorama.init()



		scope.constants.console = Rypple_Namespace({
			"fg": Rypple_Namespace({
				"black": colorama.Fore.BLACK,
				"blue": colorama.Fore.BLUE,
				"green": colorama.Fore.GREEN,
				"cyan": colorama.Fore.CYAN,
				"red": colorama.Fore.RED,
				"magenta": colorama.Fore.MAGENTA,
				"yellow": colorama.Fore.YELLOW,
				"white": colorama.Fore.WHITE,

				"lightBlack": colorama.Fore.LIGHTBLACK_EX,
				"lightBlue": colorama.Fore.LIGHTBLUE_EX,
				"lightGreen": colorama.Fore.LIGHTGREEN_EX,
				"lightCyan": colorama.Fore.LIGHTCYAN_EX,
				"lightRed": colorama.Fore.LIGHTRED_EX,
				"lightMagenta": colorama.Fore.LIGHTMAGENTA_EX,
				"lightYellow": colorama.Fore.LIGHTYELLOW_EX,
				"lightWhite": colorama.Fore.LIGHTWHITE_EX,

				"reset": colorama.Fore.RESET,
			}),

			"bg": Rypple_Namespace({
				"black": colorama.Back.BLACK,
				"blue": colorama.Back.BLUE,
				"green": colorama.Back.GREEN,
				"cyan": colorama.Back.CYAN,
				"red": colorama.Back.RED,
				"magenta": colorama.Back.MAGENTA,
				"yellow": colorama.Back.YELLOW,
				"white": colorama.Back.WHITE,

				"lightBlack": colorama.Back.LIGHTBLACK_EX,
				"lightBlue": colorama.Back.LIGHTBLUE_EX,
				"lightGreen": colorama.Back.LIGHTGREEN_EX,
				"lightCyan": colorama.Back.LIGHTCYAN_EX,
				"lightRed": colorama.Back.LIGHTRED_EX,
				"lightMagenta": colorama.Back.LIGHTMAGENTA_EX,
				"lightYellow": colorama.Back.LIGHTYELLOW_EX,
				"lightWhite": colorama.Back.LIGHTWHITE_EX,

				"reset": colorama.Back.RESET,
			}),

			"style": Rypple_Namespace({
				"bright": colorama.Style.BRIGHT,
				"dim": colorama.Style.DIM,
				"normal": colorama.Style.NORMAL,
				"resetAll": colorama.Style.RESET_ALL,
			}),
		})





	"""
		Description: ...
		Parameters: ...
	"""
	class Print(Rypple_ExtensionKey):
		name = "Print"
		enabled = True


		def callback(cls,step,scope,namespace):
			if (step.isCmd()):
				value = scope.evaluate(step.value,namespace)
				
				value = str(value)

				sys.stdout.write(value + '\n')
				sys.stdout.flush()

			else:
				return Unknown()








