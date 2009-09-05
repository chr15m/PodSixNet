from asyncore import poll2

from PodSix.SelfCallMixin import SelfCallMixin

from EndPoint import EndPoint

class Connection(EndPoint):
	def __init__(self, address=("127.0.0.1", 31425)):
		self.address = address
		self.isConnected = False
		self.queue = []
	
	def DoConnect(self, address=None):
		if not address:
			address = self.address
		EndPoint.__init__(self, address)
	
	def Close(self):
		self.close()
	
	def GetQueue(self):
		return self.queue
	
	def Pump(self):
		self.queue = []
		poll2()
	
	def Network_connected(self, data):
		self.isConnected = True
		self.queue.append({"action": "connected"})
	
	def Network(self, data):
		self.queue.append(data)
	
	def Error(self, error):
		self.queue.append({"action": "error", "error": error})
	
	def ConnectionError(self):
		self.isConnected = False
		EndPoint.ConnectionError(self)
		self.queue.append({"action": "error", "error": "Connection error"})

connection = Connection()

class ConnectionListener(SelfCallMixin):
	"""
	Subclass this guy to have your own classes monitor incoming network messages.
	"""
	def Pump(self):
		for data in connection.GetQueue():
			self.CallMethod("Network_" + data['action'], data)
			self.CallMethod("Network", data)

if __name__ == "__main__":
	from time import sleep
	class ConnectionTest(ConnectionListener):
		def Network(self, data):
			print "Network:", data
		
		def Network_error(self, error):
			print "error:", error['error']
		
		def Network_connected(self):
			print "connection test Connected"
	
	c = ConnectionTest()
	
	connection.DoConnect()
	while 1:
		connection.Pump()
		c.Pump()
		sleep(0.001)

