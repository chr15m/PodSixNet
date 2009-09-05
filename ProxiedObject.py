def ProxiedDecorator(fn):
	def new_fn(*args, **kwargs):
		[c.SendCall(args[0], fn.__name__, list(args)[1:], kwargs) for c in args[0]._proxyChannels]
		return fn(*args, **kwargs)
	return new_fn

class ProxyIdCounter:
	_counter = 0
	def GetNext(self):
		ProxyIdCounter._counter += 1
		return ProxyIdCounter._counter

class ProxiedObject(object):
	"""
		Proxied objects send all changes to themselves down a channel (probably to a server or another client).
		You must add them to the channel to be sent down, first.
		
		Any time a variable is updated it is checked in proxyVars and sent to the channel if it's there.
		Any calls that have the 'Proxied' decorator and are mirrored to the channel too.
	"""
	_proxyVars = []
	
	def __init__(self):
		self._proxyChannels = []
		#self._proxyId = ProxyIdCounter().GetNext()
		self._proxyId = id(self)
	
	def _AddChannel(self, channel):
		if not channel in self._proxyChannels:
			self._proxyChannels.append(channel)
	
	def _RemoveChannel(self, channel):
		if channel in self._proxyChannels:
			self._proxyChannels.remove(channel)
	
	def __setattr__(self, key, val):
		if key in self._proxyVars:
			[c.UpdateObject(self, {key: val}) for c in self._proxyChannels]
		
		object.__setattr__(self, key, val)

#########################
#	Test stub	#
#########################

if __name__ == "__main__":
	class DudeFace(ProxiedObject):
		_proxyVars = ['x', 'z']
		
		def __init__(self):
			ProxiedObject.__init__(self)
			self.x = 12
			self.y = ["this", "is", "cool"]
			self.z = "diggity"
		
		@ProxiedDecorator
		def MyCall(self, whatever):
			print "MyCall received", whatever
		
		def AnotherCall(self, pants):
			print "AnotherCall called with", pants
	
	class MyChannel:
		def Send(self, data):
			print "sending", data
		
		def AddObject(self, obj):
			print "adding object", obj
			self.Send({"action": "new", "class": obj.__class__.__name__, "data": obj.__dict__})
			obj._AddChannel(self)
		
		def RemoveObject(self, obj):
			print "removing object", obj
			self.Send({"action": "del", "id": obj._proxyId})
			obj._RemoveChannel(self)

		def UpdateObject(self, obj, data):
			self.Send({"action": "update", "id": obj._proxyId, "data": data})
		
		def SendCall(self, obj, method, args, kwargs):
			self.Send({"action": "call", "id": obj._proxyId, "method": method, "args": args, "kwargs": kwargs})
	
	d = DudeFace()
	d.MyCall("pants")
	d.x = 22
	
	srv = MyChannel()
	srv.AddObject(d)
	
	d.x = 45
	d.y = "mr pants"
	d.MyCall("yo")
	d.AnotherCall("eyyyyy")
	d.z = ["a", "b", 234]
	d.x = {"hello": 123, "goodbye": 55}
	
	d.z[1] = 4
	d.x["einz"] = 455

	srv.RemoveObject(d)
	
	d.x = 15
	d.MyCall("fnnnn")

