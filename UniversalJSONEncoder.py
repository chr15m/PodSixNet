from simplejson import *

class UniversalJSONEncoder(JSONEncoder):
	"""
		Adds the ability to arbitrarily encode objects to simplejson.
		
		>>> x = {"a": [2, 3, 4], "b": {"x": 5, "y": 7}, "c": ["wwra", "ww", 'rw"e']}
		>>> dumps(x, cls=UniversalJSONEncoder)
		'{"a": [2, 3, 4], "c": ["wwra", "ww", "rw\\\\"e"], "b": {"y": 7, "x": 5}}'
		
		>>> import random
		>>> t = random.Random()
		>>> t.knights = "who say ni"
		>>> dumps(t, cls=UniversalJSONEncoder)
		'["Random", {"knights": "who say ni", "gauss_next": null}]'
	"""
        def default(self, o):
		return [o.__class__.__name__, o.__dict__]

if __name__ == "__main__":
	import doctest
	doctest.testmod()
