import asyncore
import socket

from Channel import Channel

class EndPoint(Channel):
	def __init__(self, addr):
		Channel.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect(addr)
	
	def Action_connected(self, data):
		print 'got connected message', data

if __name__ == "__main__":
	from time import sleep
	class ServerChannel(Channel):
		def Action_hello(self, data):
			print "*Server* ran test method for 'hello' action"
			print "*Server* received:", data
	
	class MyEndPoint(EndPoint):
		def Action_connected(self, data):
			print "*EndPoint* received connected"
			print "*EndPoint* data:", data
	
	print "Trying failing endpoint"
	print "-----------------------"
	endpoint_bad = EndPoint(("mccormick.cx", 23342))
	for i in range(50):
		asyncore.poll2()
		sleep(0.001)
	
	from Server import Server
	server = Server(channelClass=ServerChannel)
	
	print
	print "Trying successful endpoint"
	print "--------------------------"
	
	endpoint = MyEndPoint(("localhost", 31425))
	endpoint.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	endpoint.Send({"action": "hello", "data": [454, 35, 43, 543, "aabv"]})
	endpoint.Send({"action": "hello", "data": [10] * 512})
	
	print "polling for half a second"
	for x in range(50):
		asyncore.poll2()
		sleep(0.001)

