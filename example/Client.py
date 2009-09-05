from time import time

from limugali.Connection import connection

# connection.Send({"action": "nickname", "nickname": self.parent.nameInput.text})

class Client(ConnectionListener):
	def __init__(self, game):
		self.Connect(('localhost', 31425))
	
	def Loop(self):
		ConnectionListener.Pump(self)
		self.Draw()
		
	def Draw(self):
		gfx.SetBackgroundColor([150, 150, 150])
		if not connection.isConnected and not self.errorLabel in self.objects:
			gfx.DrawText("Connecting" + ("." * ((self.frame / 10) % 4)), {"left": 0.5, "bottom": 0.7}, [200, 200, 200])
		if self.game.players:
			self.playersLabel.text = str(len(self.game.players)) + " player" + (len(self.game.players) > 1 and "s" or "") + " online"
		else:
			self.playersLabel.text = ""
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_connected(self, data):
		[self.Add(x) for x in self.uis if not x in self.objects]
	
	def Network_error(self, data):
		print data
		self.errorLabel.text = data['error'][1]
		[self.Add(x) for x in self.erroruis if not x in self.objects]
		connection.Close()
	
	def Network_disconnected(self, data):
		[self.Remove(x) for x in self.uis if x in self.objects]
		self.errorLabel.text += "\nDisconnected"
		[self.Add(x) for x in self.erroruis if not x in self.objects]

