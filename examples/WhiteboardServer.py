# find the PodSixNet module in the default situation
import sys, os; sys.path += ["..", ".." + os.path.sep + ".."];

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
		self.id = str(self._server.NextId())
		intid = int(self.id)
		self.color = [(intid + 1) % 3 * 84, (intid + 2) % 3 * 84, (intid + 3) % 3 * 84] #tuple([randint(0, 127) for r in range(3)])
		self.lines = []
	
	def PassOn(self, data):
		# pass on what we received to all connected clients
		data.update({"id": self.id})
		self._server.SendToAll(data)
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_startline(self, data):
		self.lines.append([data['point']])
		self.PassOn(data)
	
	def Network_drawpoint(self, data):
		self.lines[-1].append(data['point'])
		self.PassOn(data)

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
		player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})
		self.SendPlayers()
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": dict([(p.id, p.color) for p in self.players])})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

s = WhiteboardServer()
s.Launch()

