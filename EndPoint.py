import asyncore
import socket

from Channel import Channel

class EndPoint(Channel):
	def __init__(self, addr):
		Channel.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.connect(addr)
		except:
			print 'excepted!'
	
	def Connected(self):
		print 'connected'
	
	def Error(self):
		print "error sending"
	
	def ConnectionError(self):
		print "Couldn't connect!"

if __name__ == "__main__":
	from time import sleep
	
	def test(self, data):
		print "server received:", data
	Channel.Action_hello = test
	
	from Server import Server
	server = Server()
	
	print "Trying failing endpoint"
	print "-----------------------"
	endpoint_bad = EndPoint(("mccormick.cx", 233432))
	for i in range(100):
		asyncore.poll2()
		sleep(0.1)
	
	print "Trying successful endpoint"
	print "--------------------------"
	
	endpoint = EndPoint(("localhost", 31425))
	endpoint.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	endpoint.Send({"action": "hello", "data": [454, 35, 43, 543, "aabv"]})
	endpoint.Send({"action": "hello", "data": [10] * 512})
	
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass

