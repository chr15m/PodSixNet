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
		channel.Send({"action": "connected"})
		if hasattr(self, "Connected"):
			self.Connected(conn, addr)

#########################
#	Test stub	#
#########################

if __name__ == "__main__":
	class ServerChannel(Channel):
		def Action_hello(self, data):
			print "*Server* ran test method for 'hello' action"
			print "*Server* received:", data
	
	class EndPointChannel(Channel):
		def Action_connected(self, data):
			print "*EndPoint* ran connected method"
			print "*EndPoint* received:", data
			print "*EndPoint* initiating send"
			outgoing.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	
	server = Server(channelClass=ServerChannel)
	
	sender = asyncore.dispatcher()
	sender.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	sender.connect(("localhost", 31425))
	outgoing = EndPointChannel(sender)
	
	from time import sleep
	
	print "\tpolling for half a second"
	for x in range(50):
		asyncore.poll2()
		sleep(0.001)

