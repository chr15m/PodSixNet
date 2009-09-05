from PodSix.SelfCallMixin import SelfCallMixin

from EndPoint import EndPoint

connection = EndPoint()

class ConnectionListener(SelfCallMixin):
	"""
	Subclass this guy to have your own classes monitor incoming network messages.
	"""
	def Connect(self, *args, **kwargs):
		connection.DoConnect(*args, **kwargs)
		# check for connection errors:
		self.Pump()
	
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
		
		def Network_connected(self, data):
			print "connection test Connected"
	
	c = ConnectionTest()
	
	c.Connect()
	while 1:
		connection.Pump()
		c.Pump()
		sleep(0.001)

