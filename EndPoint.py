# coding=utf-8
import socket
import sys

if float(sys.version[:3]) < 2.5:
	from asyncore import poll2 as poll
else:
	from asyncore import poll

from Channel import Channel

class EndPoint(Channel):
	"""
	The endpoint queues up all network events for other classes to read.
	"""
	def __init__(self, address=("127.0.0.1", 31425)):
		self.address = address
		self.isConnected = False
		self.queue = []
	
	def DoConnect(self, address=None):
		if address:
			self.address = address
		try:
			Channel.__init__(self)
			self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connect(self.address)
		except socket.gaierror, e:
			self.queue.append({"action": "error", "error": e.args})
	
	def GetQueue(self):
		return self.queue
	
	def Pump(self):
		Channel.Pump(self)
		self.queue = []
		poll()
	
	# methods to add network data to the queue depending on network events
	
	def Close(self):
		self.isConnected = False
		self.close()
		self.queue.append({"action": "disconnected"})
	
	def Connected(self):
		self.queue.append({"action": "socketConnect"})
	
	def Network_connected(self, data):
		self.isConnected = True
	
	def Network(self, data):
		self.queue.append(data)
	
	def Error(self, error):
		self.queue.append({"action": "error", "error": error})
	
	def ConnectionError(self):
		self.isConnected = False
		self.queue.append({"action": "error", "error": (-1, "Connection error")})

if __name__ == "__main__":
	from time import sleep
	class ServerChannel(Channel):
		def Network_hello(self, data):
			print "*Server* ran test method for 'hello' action"
			print "*Server* received:", data
			self.Send({"action": "gotit", "data": "Yeah, we got it: " + str(len(data['data'])) + " elements"})
	
	print "Trying failing endpoint"
	print "-----------------------"
	endpoint_bad = EndPoint(("mccormick.cx", 23342))
	endpoint_bad.DoConnect()
	for i in range(50):
		endpoint_bad.Pump()
		if endpoint_bad.GetQueue():
			print endpoint_bad.GetQueue()
		sleep(0.001)
	
	from Server import Server
	server = Server(channelClass=ServerChannel)
	
	print
	print "Trying successful endpoint"
	print "--------------------------"
	
	endpoint = EndPoint(("localhost", 31425))
	endpoint.DoConnect()
	endpoint.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	endpoint.Send({"action": "hello", "data": [454, 35, 43, 543, "aabv"]})
	endpoint.Send({"action": "hello", "data": [10] * 512})
	endpoint.Send({"action": "hello", "data": [10] * 512, "otherstuff": "hello\0---\0goodbye", "x": [0, "---", 0], "y": "zäö"})
	
	print "polling for half a second"
	for x in range(50):
		server.Pump()
		endpoint.Pump()
		if endpoint.GetQueue():
			print "*Endpoint*:", endpoint.GetQueue()
		sleep(0.001)
	
	endpoint.Close()
	print endpoint.GetQueue()
