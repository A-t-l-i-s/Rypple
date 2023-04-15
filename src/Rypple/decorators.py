__all__ = "Name", "Description", "Enabled", "Value"





class Name:
	def __init__(self,text):
		self.text = text



	def __call__(self,obj):
		obj.name = self.text
		
		return obj





class Description:
	def __init__(self,text):
		self.text = text



	def __call__(self,obj):
		obj.description = self.text
		
		return obj





class Enabled:
	def __init__(self,enabled=True):
		self.enabled = enabled



	def __call__(self,obj):
		obj.enabled = self.enabled

		return obj





class Value:
	def __init__(self,name,value):
		self.name = name
		self.value = value



	def __call__(self,obj):
		try:
			setattr(obj,self.name,self.value)
		except:
			...

		return obj











