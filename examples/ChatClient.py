# find the PodSixNet module in the default situation
import sys, os; sys.path += ["..", ".." + os.path.sep + ".."];

from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import *

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *

class Client(ConnectionListener):
	def __init__(self):
		self.Connect(('localhost', 31425))
		print "Chat client started"
		print "Ctrl-C to exit"
		# get a nickname from the user before starting
		print "Enter your nickname: ",
		connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})
		# launch our threaded input loop
		t = start_new_thread(self.InputLoop, ())
	
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	def InputLoop(self):
		# horrid threaded input loop
		# continually reads from stdin and sends whatever is typed to the server
		while 1:
			connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
	
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	def Network_players(self, data):
		print "*** players: " + ", ".join([p for p in data['players']])
	
	def Network_message(self, data):
		print data['who'] + ": " + data['message']
	
	# built in stuff

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

c = Client()
while 1:
	c.Loop()
	sleep(0.001)
