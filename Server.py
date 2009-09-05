import asyncore
import socket

from Channel import Channel

class Server(asyncore.dispatcher):
	def __init__(self, channelClass=Channel, localaddr=("127.0.0.1", 31425), listeners=5):
		self.channelClass = channelClass
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(localaddr)
		self.listen(listeners)
	
	def handle_accept(self):
		# TODO: generate a random ID and send it through for the client to adopt
		conn, addr = self.accept()
		channel = self.channelClass(conn, addr, self)
		if hasattr(self, "Connected"):
			self.Connected(conn, addr)

#########################
#	Test stub	#
#########################

if __name__ == "__main__":
	def test(self, data):
		print "Ran test method for 'hello' action"
		print "received:", data
	Channel.Action_hello = test
	
	server = Server()
	
	sender = asyncore.dispatcher()
	sender.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	sender.connect(("localhost", 31425))
	
	outgoing = Channel(sender)
	outgoing.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass

