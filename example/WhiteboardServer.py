from time import sleep, localtime
from random import randint
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ServerChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.id = self._server.NextId()
		self.color = tuple([randint(0, 127) for r in range(3)])
		self.lines = []
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_draw(self, data):
		print "Client", self, "drew a point at", data['point']

class WhiteboardServer(Server):
	channelClass = ServerChannel
	
	def __init__(self, *args, **kwargs):
		self.id = 0
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print 'Server launched'
	
	def NextId(self):
		self.id += 1
		return self.id
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def AddPlayer(self, player):
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		player.Send({"action": "initial", "lines": dict([(p.id, (p.color, p.lines)) for p in self.players])})
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.id for p in self.players]})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

s = WhiteboardServer()
s.Launch()

