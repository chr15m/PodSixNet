import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

class LagTimeClient(ConnectionListener):
	""" This example client connects to a LagTimeServer which then sends pings back.
	This client responds to 10 pings, and the server measures the round-trip time of each ping and outputs it."""
	def __init__(self, host, port):
		self.Connect((host, port))
		print "LagTimeClient started"
	
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	def Network_ping(self, data):
		print "got:", data
		if data["count"] == 10:
			connection.Close()
		else:
			connection.Send(data)
	
	# built in stuff
	
	def Network_connected(self, data):
		print "Connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = LagTimeClient(host, int(port))
	while 1:
		connection.Pump()
		c.Pump()
		sleep(0.001)
