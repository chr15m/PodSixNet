from simplejson import *

class UniversalJSONEncoder(JSONEncoder):
        def default(self, o):
		return [o.__class__.__name__, o.__dict__]

if __name__ == "__main__":
        class NewClass:
                def __init__(self):
			self.wigg = 123
			self.hello = "Mr. Pants"
	
	x = {"a": [2, 3, 4], "b": {"x": 5, "y": 7}, "c": ["wwra", "ww", 'rw"e']}
	print dumps(x, cls=UniversalJSONEncoder)
	
	x = NewClass()
	print dumps(x, cls=UniversalJSONEncoder)

