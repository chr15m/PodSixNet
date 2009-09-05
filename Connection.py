from EndPoint import EndPoint

connection = EndPoint()

class ConnectionListener:
	"""
	Looks at incoming data and calls matching methods in self based on what comes in.
	Subclass this to have your own classes monitor incoming network messages.
	"""
	def Connect(self, *args, **kwargs):
		connection.DoConnect(*args, **kwargs)
		# check for connection errors:
		self.Pump()
	
	def Pump(self):
		for data in connection.GetQueue():
			[getattr(self, n)(data) for n in ("Network_" + data['action'], "Network") if hasattr(self, n)]

if __name__ == "__main__":
	from time import sleep
	from sys import exit
	class ConnectionTest(ConnectionListener):
		def Network(self, data):
			print "Network:", data
		
		def Network_error(self, error):
			print "error:", error['error']
			print "Did you start a server?"
			exit(-1)
		
		def Network_connected(self, data):
			print "connection test Connected"
	
	c = ConnectionTest()
	
	c.Connect()
	while 1:
		connection.Pump()
		c.Pump()
		sleep(0.001)

