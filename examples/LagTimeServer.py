from time import sleep, localtime
from weakref import WeakKeyDictionary
from time import time
import sys

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class LagTimeChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.count = 0
		self.times = []
	
	def Close(self):
		print self, 'Client disconnected'
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_ping(self, data):
		print self, "ping %d round trip time was %f" % (data["count"], time() - self.times[data["count"]])
		self.Ping()
	
	def Ping(self):
		print self, "Ping:", self.count
		self.times.append(time())
		self.Send({"action": "ping", "count": self.count})
		self.count += 1

class LagTimeServer(Server):
	channelClass = LagTimeChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		print 'Server launched'
	
	def Connected(self, channel, addr):
		print channel, "Channel connected"
		channel.Ping()
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	s = LagTimeServer(localaddr=(host, int(port)))
	s.Launch()

