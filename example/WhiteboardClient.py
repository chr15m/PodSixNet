from time import sleep

from PodSixNet.Connection import *
from Whiteboard import Whiteboard

class Client(ConnectionListener, Whiteboard):
	def __init__(self):
		self.Connect(('localhost', 31425))
		Whiteboard.__init__(self)
	
	def Loop(self):
		connection.Pump()
		self.Pump()
		self.Events()
		self.Draw()
		
		if "connecting" in self.status:
			self.status = "connecting" + ("." * ((self.frame / 30) % 4))
	
	#######################	
	### Event callbacks ###
	#######################
	def PenDraw(self, e):
		connection.Send({"action": "draw", "point": e.pos})
	
	###############################
	### Network event callbacks ###
	###############################
	
	def Network(self, data):
		print 'network:', data
	
	def Network_connected(self, data):
		print 'connected:', data
	
	def Network_error(self, data):
		print 'error:', data
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'disconnected'

c = Client()
while 1:
	c.Loop()
	sleep(0.001)
