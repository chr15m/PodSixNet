import asyncore
import socket

from Channel import Channel

class EndPoint(Channel):
	def __init__(self, addr):
		self._socket = asyncore.dispatcher()
		self._socket.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect(addr)
		Channel.__init__(self, self._socket, addr)

if __name__ == "__main__":
	def test(self, data):
		print "server received:", data
	Channel.Action_hello = test
	
	from Server import Server
	server = Server()
	
	endpoint = EndPoint(("localhost", 31425))
	endpoint.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	endpoint.Send({"action": "hello", "data": [454, 35, 43, 543, "aabv"]})
	endpoint.Send({"action": "hello", "data": [10] * 512})
	
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass

