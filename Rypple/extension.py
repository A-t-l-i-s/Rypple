import inspect

from .decorators import *





__all__ = ("Rypple_Extension",)





requiredParameters = (
	"cls",
	"step",
	"scope",
	"namespace"
)





class Rypple_Extension:
	name: str = None
	description: str = None

	enabled: bool = False
	core: bool = False



	def init(cls,scope):
		...




	# ~~~~~~~~~~~~ Methods ~~~~~~~~~~~
	@classmethod
	def all(cls):
		funcs = {}


		for d in dir(cls):
			v = getattr(cls,d)
			
			if (not (d.startswith("__") and d.endswith("__"))):
				if (cls.valid(v)):
					enabled = True

					# If enabled
					if (hasattr(v,"enabled")):
						if (not v.enabled):
							enabled = False


					if (enabled):
						# Get name
						if (hasattr(v,"name")):
							name = v.name
						
						else:
							name = d

						# Add function
						funcs[name] = v


		return funcs






	@classmethod
	def get(cls,name):
		funcs = cls.all()

		return funcs.get(name)





	@classmethod
	def valid(cls,func):
		if (callable(func)):
			try:
				sig = inspect.signature(func)
				args = tuple(sig.parameters)

			except:
				return False


			if (args == requiredParameters):
				if (func.enabled):
					return True


		return False
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~










