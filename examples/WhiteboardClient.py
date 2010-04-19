import sys
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener
from Whiteboard import Whiteboard

class Client(ConnectionListener, Whiteboard):
	def __init__(self, host, port):
		self.Connect((host, port))
		self.players = {}
		Whiteboard.__init__(self)
	
	def Loop(self):
		self.Pump()
		connection.Pump()
		self.Events()
		self.Draw([(self.players[p]['color'], self.players[p]['lines']) for p in self.players])
		
		if "connecting" in self.statusLabel:
			self.statusLabel = "connecting" + ("." * ((self.frame / 30) % 4))
	
	#######################	
	### Event callbacks ###
	#######################
	#def PenDraw(self, e):
	#	connection.Send({"action": "draw", "point": e.pos})
	
	def PenDown(self, e):
		connection.Send({"action": "startline", "point": e.pos})
	
	def PenMove(self, e):
		connection.Send({"action": "drawpoint", "point": e.pos})
	
	def PenUp(self, e):
		connection.Send({"action": "drawpoint", "point": e.pos})
	
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
		print data
		import traceback
		traceback.print_exc()
		self.statusLabel = data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		self.statusLabel += " - disconnected"

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	while 1:
		c.Loop()
		sleep(0.001)

