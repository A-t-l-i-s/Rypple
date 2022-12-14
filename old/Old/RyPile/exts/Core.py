import sys
import re
import os
import json
import time
import shlex
import ntpath

from ..BaseExtension import *





__all__=["Extension"]





class Extension(BaseExtension):
	enabled=True

	name="Core"

	executable=None
	extensions=()



	# ~~~~~~~~~~~ Variables ~~~~~~~~~~
	"""
		Description: Sets the current directory
		Parameters: path:str[required]
	"""
	class Path(BaseExtensionKey):
		enabled=True
		name="Path"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				if (ntpath.exists(value) and ntpath.isdir(value)):
					# Change directory
					os.chdir(value)
					scope.path=ntpath.realpath(value)

				else:
					... # Error
			else:
				... # Error





	"""
		Description: Adds extra arguments to the extension
		Parameters: args:list[str][required]
	"""
	class Extra(BaseExtensionKey):
		enabled=True
		name="Extra"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])


			if (isinstance(value,str)):
				# Split into shell args
				args=shlex.split(value)


				scope.extra+=args

			else:
				... # Error





	"""
		Description: Specifies if any external processes are created with a new console
		Parameters: value:bool[required]
	"""
	class Popout(BaseExtensionKey):
		enabled=True
		name="Popout"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,bool)):
				scope.popout=value


			elif (value == None):
				scope.popout=True


			else:
				... # Error





	"""
		Description: Specifies the current extension
		Parameters: ext:str[required]
	"""
	class Extension(BaseExtensionKey):
		enabled=True
		name="Extension"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				if (value in parent.extensions):
					scope.extension=parent.extensions[value]

				else:
					... # Error
			else:
				... # Error





	"""
		Description: Specifies the extension executable
		Parameters: path:str[required]
	"""
	class Executable(BaseExtensionKey):
		enabled=True
		name="Executable"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				if (ntpath.exists(value) and ntpath.isfile(value)):
					if (scope != None):
						scope.extension.executable=value

					else:
						... # Error
				else:
					... # Error
			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Commands ~~~~~~~~~~~
	"""
		Description: Pauses the compilation process to start a new external process
		Parameters: args:list[str][required]
	"""
	class Run(BaseExtensionKey):
		enabled=True
		name="Run"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				# Split into shell args
				args=shlex.split(value)

				if (not parent.process(scope,args)):
					... # Error
			else:
				... # Error





	"""
		Description: Delays the compilation process at the current line
		Parameters: secs:float[required]
	"""
	class Delay(BaseExtensionKey):
		enabled=True
		name="Delay"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				deltas=(
					("ns",1 / 1000 / 1000),
					("ms",1 / 1000),
					("s",1),
					("m",60),
					("h",60 * 60),
					("d",60 * 60 * 24),
				)


				# Find ending delta for value
				delta=None
				for d in deltas:
					if (value.endswith(d[0])):
						delta=d
						break


				# If no delta found
				if (delta != None):
					t=value[:-len(delta[0])]

				else:
					t=value
					delta=["s",1]


				# Convert to number
				if (isinstance((v:=scope.evaluate(t)),(int,float))):
					secs=v * delta[1]

					# Delay program
					time.sleep(secs)

				else:
					... # Error
			else:
				... # Error





	"""
		Description: Adds steps from specified file into the current scope
		Parameters: path:str[required]
	"""
	class Include(BaseExtensionKey):
		enabled=True
		name="Include"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				v1=value + ".rypl"
				if (ntpath.exists(v1) and ntpath.isfile(v1)):
					value=v1


				if (ntpath.exists(value) and ntpath.isfile(value)):
					loaded=False

					for s in scope.steps:
						if (ntpath.samefile(s["file"],value)):
							loaded=True
							break


					if (not loaded):
						steps=parent.getSteps(value)

						if (steps != None):
							i=scope.index + 1
							scope.steps[i:i]=steps

						else:
							... # Error
					else:
						... # Error
				else:
					... # Error
			else:
				... # Error





	"""
		Description: Deletes variable from scope
		Parameters: var:str[required]
	"""
	class Delete(BaseExtensionKey):
		enabled=True
		name="Delete"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			if (isinstance(value,str)):
				# If value in scope
				if (value in scope.data):
					scope.data.pop(value)

				else:
					... # Error
			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Statements ~~~~~~~~~~
	"""
		Description: Compiles current extension
		Parameters: None
	"""
	class Done(BaseExtensionKey):
		enabled=True
		name="Done"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				if ((ext:=scope.extension) != None):
					try:
						ext.execute(ext,parent,scope)
					
					except:
						... # Error
				else:
					... # Error
			else:
				... # Error





	"""
		Description: Exit breaks the compilation loop
		Parameters: None
	"""
	class Exit(BaseExtensionKey):
		enabled=True
		name="Exit"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				scope.exit=True

			else:
				... # Error





	"""
		Description: Ignores this step
		Parameters: None
	"""
	class Pass(BaseExtensionKey):
		enabled=True
		name="Pass"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				...

			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	


	# ~~~~~~~~~~~~ Console ~~~~~~~~~~~
	"""
		Description: Prints data to the console
		Parameters: text:str[required]
	"""
	class Print(BaseExtensionKey):
		enabled=True
		name="Print"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])
			value=scope.evaluate(value)


			sys.stdout.write(str(value) + "\n")
			sys.stdout.flush()





	"""
		Description: Clears the console
		Parameters: None
	"""
	class Clear(BaseExtensionKey):
		enabled=True
		name="Clear"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				...
			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~ Conditions ~~~~~~~~~~
	"""
		Description: Conditional if statement
		Parameters: condition:str[required]
	"""
	class If(BaseExtensionKey):
		enabled=True
		name="If"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])


			if (isinstance(value,str)):
				if (scope.evaluate(value)):
					...

				else:
					if (scope.skipTo([extension.Else.name,extension.End.name])):
						...

					else:
						... # Error
			else:
				... # Error





	"""
		Description: Conditional else statement
		Parameters: None
	"""
	class Else(BaseExtensionKey):
		enabled=True
		name="Else"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				if (scope.skipTo(extension.End.name)):
					...

				else:
					... # Error
			else:
				... # Error





	"""
		Description: Signals that the end of the if/for/while/function statement
		Parameters: None
	"""
	class End(BaseExtensionKey):
		enabled=True
		name="End"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				...

			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~ Function ~~~~~~~~~~~
	"""
		Description: Declares a callable function
		Parameters: name:str[required]
	"""
	class Function(BaseExtensionKey):
		enabled=True
		name="Function"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])


			if (isinstance(value,str)):
				scope[value]=step["id"]
				if (scope.skipTo(extension.End.name)):
					...

				else:
					... # Error
			else:
				... # Error




	"""
		Description: Declares a label
		Parameters: name:str[required]
	"""
	class Label(BaseExtensionKey):
		enabled=True
		name="Label"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])


			if (isinstance(value,str)):
				scope[value]=step["id"]

			else:
				... # Error





	"""
		Description: Returns to the line in which the function/label as called
		Parameters: None
	"""
	class Return(BaseExtensionKey):
		enabled=True
		name="Return"

		def callback(extension,parent,scope,step):
			value=step["value"]


			if (value == None):
				if (len(scope.steps)>0):
					# Pop latest call
					u=scope.calls.pop(-1)


					# Find line by uuid
					i,s=scope.findLine(u)


					# If found uuid
					if (i > -1):
						scope.index=i

			else:
				... # Error





	"""
		Description: Calls a function
		Parameters: name:str[required]
	"""
	class Call(BaseExtensionKey):
		enabled=True
		name="Call"

		def callback(extension,parent,scope,step):
			value=scope.format(step["value"])


			if (isinstance(value,str)):
				if ((v:=scope.data.get(value)) != None):
					# Find line by uuid
					i,s=scope.findLine(v)


					if (s["key"]==extension.Function.name or s["key"] == extension.Label.name):
						# If found uuid
						if (i > -1):
							scope.index=i
							scope.calls.append(step["id"])



			else:
				... # Error
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~~~~~ Looping ~~~~~~~~~~~
	"""
		Description: Loops until the condition is false
		Parameters: condition:str[required]
	"""
	class While(BaseExtensionKey):
		enabled=True
		name="While"

		def callback(extension,parent,scope,step):
			...





	"""
		Description: Iterates through each item in a list 
		Parameters: arr:list[required]
	"""
	class Foreach(BaseExtensionKey):
		enabled=True
		name="Foreach"

		def callback(extension,parent,scope,step):
			...
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

