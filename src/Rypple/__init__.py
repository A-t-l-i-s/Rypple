import re
import uuid

from pathlib import Path

from RFTLib.Core.Structure import *

from .scope import *
from .extension import *





__all__ = ("Rypple", "Rypple_Scope", "Rypple_Extension")





class Rypple:
	# ~~~~~~~~~~ Variables ~~~~~~~~~~~
	maxLevel: int = 9999

	delimiter: str = ":"

	tempChar: str = "~"
	threadChar: str = "*"
	commandChar: str = "@"
	
	macroChar: str = "$"
	joinerChar: str = "^"
	commentChar: str = ">"


	macros:dict = {}
	includedFiles:list = []
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	


	# ~~~~~~~~~~~~ Paths ~~~~~~~~~~~~~
	includePaths:list = []

	fileExtensions:list = [
		".ryp",
		".rypl",

		".ryc",
		".rycl",
	]
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~~~ Regex Patterns ~~~~~~~~
	keyPattern: re.Pattern = re.compile(
		r"[A-Za-z\_][\w\.]*"
	)

	signsPattern: re.Pattern = re.compile(
		rf"[{tempChar}{threadChar}{commandChar}]*"
	)

	framePattern: re.Pattern = re.compile("".join((
		r"^(?P<Level>\s*)",
			rf"(?P<Signs>{signsPattern.pattern})",
			rf"(?P<Key>{keyPattern.pattern})",
				rf"((\s*)({delimiter})(\s*)(?P<Value>.*))?",
		r"(\s*)$",
	)))
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



	# ~~~~~~ Structure Defaults ~~~~~~
	frameDefaults = RFT_Structure({
		"key": None,
		"value": None,
		"id": -1,
		"level": -1,

		"temp": False,
		"thread": False,
		"command": False,

		"children": []
	})
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





	@classmethod
	def readFile(cls, path):
		path = Path(path)

		if (path.exists() and path.is_file()):
			with path.open("r") as file:
				data = file.read()

			# Split data into lines
			lines = cls.toLines(data)

			base = cls.toFrames(lines)

			return base
		else:
			raise OSError("File doesn't exist.")





	@classmethod
	def toLines(cls, data):
		lines = []

		for line in data.split("\n"):
			lineStrip = line.strip()
			
			if (lineStrip):
				if (not lineStrip.startswith(cls.commentChar)):
					# If line belongs to previous line
					if (lineStrip.startswith(cls.joinerChar)):
						# Get joiner index
						index = line.index(cls.joinerChar)
						
						# Remove spacing and joiner character
						newLine = line[index + 1:]

						# If not first line
						if (len(lines) > 0):
							lines[-1] += newLine
						else:
							lines.append(newLine)
					else:
						lines.append(line)


		return lines





	@classmethod
	def toFrames(cls, lines:list | str):
		base = RFT_Structure(
			{
				"key": "Base"
			},
			defaults = cls.frameDefaults
		)


		hierarchy = [base]
		previous = base



		# If lines in a single string
		if (isinstance(lines, str)):
			lines = [lines]



		# Iterate through all lines
		for line in lines:
			# Add macro values to line
			for k,v in cls.macros.items():				
				# Replace macro with value
				line = re.sub(
					rf"\{cls.macroChar}\[\s*{k}\s*\]", # Pattern
					v, # Replace Value
					line # Input String
				)



			# Regex match to frame pattern
			match = cls.framePattern.match(line)

			if (match):
				# Get groups
				levelGroup = match.group("Level")
				signsGroup = match.group("Signs")
				
				key = match.group("Key")
				value = match.group("Value")



				# If value is present
				if (value != None):
					value = value.strip()

				# f values length is nothing due to strip
				if (not value):
					value = None



				if (key):
					# Get level
					level = 0
					level += levelGroup.count(" ")
					level += levelGroup.count("\t")



					# Create new id
					idUUID = uuid.uuid1()
					id_ = idUUID.hex.lower()



					# Get default signs
					temp = cls.frameDefaults.temp
					thread = cls.frameDefaults.thread
					command = cls.frameDefaults.command


					# Temp sign
					if (cls.tempChar in signsGroup):
						temp = not temp

					# Thread sign
					if (cls.threadChar in signsGroup):
						thread = not thread

					# Command sign
					if (cls.commandChar in signsGroup):
						command = not command



					if (level <= cls.maxLevel):
						# All frames that will be processed
						frames = []



						# Create new step
						firstFrame = RFT_Structure(
							{
								"key": key,
								"value": value,
								"id": id_,
								"level": level,
								
								"temp": temp,
								"thread": thread,
								"command": command,
							},
							defaults = cls.frameDefaults
						)



						if (key == "Include" and command):
							path = Path(value)
							path = path.resolve()

							if (path not in cls.includedFiles):
								cls.includedFiles.append(path)
							
								# If path exists and is a file
								if (path.exists() and path.is_file()):
									# Read file
									includeBase = cls.readFile(path)

									# Add frames to current children
									frames += includeBase.children



						elif (key == "Macro" and command):
							macroBase = cls.toFrames(value)

							# If successfully parsed enough frames
							if (len(macroBase.children) > 0):
								# Get first child
								macroFrame = macroBase.children[0]

								# Add macro to list of macros
								cls.macros[macroFrame.key] = macroFrame.value


						else:
							frames.append(firstFrame)



						# Iterate through all frames
						for frame in frames:
							hlen = len(hierarchy)


							if (level >= hlen):
								dif = (level - hlen) + 1
								hierarchy += [base] * dif


							if (level == previous.level + 1):
								hierarchy[level - 1] = previous


							parent = hierarchy[level - 1]
							if (parent != None):
								parent.children.append(frame)


							previous = frame


		return base






