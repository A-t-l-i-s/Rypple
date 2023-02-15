import json
import pathlib





__all__=["Rypple_JSON_Encoder"]





class Rypple_JSON_Encoder(json.JSONEncoder):
	def default(self,obj):
		out = None



		if (isinstance(obj,pathlib.Path)):
			out = str(obj.resolve())



		return out









