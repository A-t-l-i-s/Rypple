import datetime
import colorama

colorama.init()

RESET = colorama.Fore.RESET
RED = colorama.Fore.LIGHTRED_EX
CYAN = colorama.Fore.LIGHTCYAN_EX
BLUE = colorama.Fore.LIGHTBLUE_EX
GRAY = colorama.Fore.LIGHTBLACK_EX
WHITE = colorama.Fore.LIGHTWHITE_EX
YELLOW = colorama.Fore.LIGHTYELLOW_EX

sep1_1 = f"{GRAY}[{RESET}"
sep1_2 = f"{GRAY}]{RESET}"

sep2_1 = f"{GRAY}({RESET}"
sep2_2 = f"{GRAY}){RESET}"

deli = f"{GRAY}:{RESET}"





__all__ = "Rypple_Exception", "Rypple_Critical", "Rypple_Error", "Rypple_Warning", "Rypple_Log"





class Rypple_Exception:
	def __init__(self,text=""):
		self.text = f"{self.now()}{deli} {WHITE}{text}"



	def time(self):
		# Get current time
		now = datetime.datetime.now()

		# Format time
		out = f"{sep1_1}{CYAN}{now.hour:<2}:{now.minute:<2}:{str(now.second) + '.' + str(now.microsecond)[:2]:<5}{sep1_2}"

		return out



	@classmethod
	def NoValue(cls):
		return Rypple_Error("No value present")


	@classmethod
	def HasValue(cls):
		return Rypple_Error("Can't accept values")


	@classmethod
	def TypeError(cls,t):
		return Rypple_Error(f"Invalid type '{t.__name__}'")








class Rypple_Critical(Rypple_Exception):
	def __init__(self,text=""):
		self.text = f"{self.time()} {sep2_1}{RED}Critical{sep2_2}{deli} {WHITE}{text}"





class Rypple_Error(Rypple_Exception):
	def __init__(self,text=""):
		self.text = f"{self.time()} {sep2_1}{RED}Error{sep2_2}{deli} {WHITE}{text}"





class Rypple_Warning(Rypple_Exception):
	def __init__(self,text=""):
		self.text = f"{self.time()} {sep2_1}{YELLOW}Warning{sep2_2}{deli} {WHITE}{text}"





class Rypple_Log(Rypple_Exception):
	def __init__(self,text=""):
		self.text = f"{self.time()} {sep2_1}{BLUE}Log{sep2_2}{deli} {WHITE}{text}"






