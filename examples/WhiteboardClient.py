from time import sleep

from PodSixNet.Connection import *
from Whiteboard import Whiteboard

class Client(ConnectionListener, Whiteboard):
	def __init__(self):
		self.Connect(('localhost', 31425))
		self.players = {}
		Whiteboard.__init__(self)
		self.sendqueue = []
	
	def Loop(self):
		connection.Pump()
		self.Pump()
		self.Events()
		[connection.Send(x) for x in self.sendqueue]
		self.sendqueue = []
		self.Draw([(self.players[p]['color'], self.players[p]['lines']) for p in self.players])
		
		if "connecting" in self.statusLabel:
			self.statusLabel = "connecting" + ("." * ((self.frame / 30) % 4))
	
	#######################	
	### Event callbacks ###
	#######################
	#def PenDraw(self, e):
	#	connection.Send({"action": "draw", "point": e.pos})
	
	def PenDown(self, e):
		self.sendqueue.append({"action": "startline", "point": e.pos})
	
	def PenMove(self, e):
		self.sendqueue.append({"action": "drawpoint", "point": e.pos})
	
	def PenUp(self, e):
		self.sendqueue.append({"action": "drawpoint", "point": e.pos})
	
	###############################
	### Network event callbacks ###
	###############################
	
	def Network_initial(self, data):
		self.players = data['lines']
	
	def Network_drawpoint(self, data):
		self.players[data['id']]['lines'][-1].append(data['point'])
	
	def Network_startline(self, data):
		self.players[data['id']]['lines'].append([data['point']])
	
	def Network_players(self, data):
		self.playersLabel = str(len(data['players'])) + " players"
		mark = []
		
		for i in data['players']:
			if not self.players.has_key(i):
				self.players[i] = {'color': data['players'][i], 'lines': []}
		
		for i in self.players:
			if not i in data['players'].keys():
				mark.append(i)
		
		for m in mark:
			del self.players[m]
	
	def Network(self, data):
		#print 'network:', data
		pass
	
	def Network_connected(self, data):
		self.statusLabel = "connected"
	
	def Network_error(self, data):
		self.statusLabel = data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		self.statusLabel += " - disconnected"

c = Client()
while 1:
	c.Loop()
	sleep(0.001)
