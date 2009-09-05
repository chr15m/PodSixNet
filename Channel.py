import asynchat

from UniversalJSONEncoder import *

class Channel(asynchat.async_chat):
	def __init__(self, conn=None, addr=(), server=None):
		asynchat.async_chat.__init__(self, conn=conn)
		self.addr = addr
		self._server = server
		self._ibuffer = ""
		self.set_terminator("\0")
	
	def collect_incoming_data(self, data):
		self._ibuffer += data
	
	def found_terminator(self):
		data = loads(self._ibuffer)
		self._ibuffer = ""
		
		if data.has_key('action'):
			method = getattr(self, 'Action_' + data['action'], None)
			if method:
				method(data)
	
	def Send(self, data):
		asynchat.async_chat.push(self, dumps(data, cls=UniversalJSONEncoder) + "\0")
	
	def handle_connect(self):
		if self.connected and hasattr(self, "Connected"):
			self.Connected()
	
	def handle_expt(self):
		self.close()
		if hasattr(self, "ConnectionError"):
			self.ConnectionError()
	
	def handle_error(self):
		if hasattr(self, "Error"):
			self.Error()
