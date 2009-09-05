from time import sleep, localtime
from weakref import WeakKeyDictionary

from limugali.Server import Server
from limugali.Channel import Channel

class ServerChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		self.nickname = "anonymous"
		self.away = False
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################

	def Network_message(self, data):
		self._server.SendToAll({"action": "message", "message": self.nickname + ": " + data['message']})
	
	def Network_nickname(self, data):
		self.nickname = data['nickname']
		self._server.SendPlayers()
	
	def Network_away(self, data):
		self.away = data['away']
		self._server.SendPlayers()

class CCServer(Server):
	channelClass = ServerChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def AddPlayer(self, player):
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		print "players", [p for p in self.players]
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [(p.nickname, p.away) for p in self.players]})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

s = CCServer()
s.Launch()

