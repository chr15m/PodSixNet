import asynchat
import sys, traceback

from rencode import loads, dumps

class Channel(asynchat.async_chat):
	endchars = '\0---\0'
	def __init__(self, conn=None, addr=(), server=None):
		asynchat.async_chat.__init__(self, conn)
		self.addr = addr
		self._server = server
		self._ibuffer = ""
		self.set_terminator(self.endchars)
		self.sendqueue = []
	
	def collect_incoming_data(self, data):
		self._ibuffer += data
	
	def found_terminator(self):
		data = loads(self._ibuffer)
		self._ibuffer = ""
		
		if type(dict()) == type(data) and data.has_key('action'):
			[getattr(self, n)(data) for n in ('Network_' + data['action'], 'Network') if hasattr(self, n)]
		else:
			print "OOB data:", data
	
	def Pump(self):
		[asynchat.async_chat.push(self, d) for d in self.sendqueue]
		self.sendqueue = []
	
	def Send(self, data):
		self.sendqueue.append(dumps(data) + self.endchars)
	
	def handle_connect(self):
		if hasattr(self, "Connected"):
			self.Connected()
		else:
			print "Unhandled Connected()"
	
	def handle_error(self):
		try:
			self.close()
		except:
			pass
		if hasattr(self, "Error"):
			self.Error(sys.exc_info()[1])
		else:
			asynchat.async_chat.handle_error(self)
	
	def handle_expt(self):
		pass
	
	def handle_close(self):
		if hasattr(self, "Close"):
			self.Close()
		asynchat.async_chat.handle_close(self)

