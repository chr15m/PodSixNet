PodSixNet - lightweight multiplayer networking library for Python games
-----------------------------------------------------------------------

PodSixNet is a lightweight network layer designed to make it easy to write multiplayer games in Python. It uses Python's built in asyncore library and rencode.py (included) to asynchronously serialise network events and arbitrary data structures, and deliver them to your high level classes through simple callback methods.

Each class within your game client which wants to receive network events, subclasses the ConnectionListener class and then implements `Network_*` methods to catch specific user-defined events from the server. You don't have to wait for buffers to fill, or check sockets for waiting data or anything like that, just do `connection.Pump()` once per game loop and the library will handle everything else for you, passing off events to all classes that are listening. Sending data back to the server is just as easy, using `connection.Send(mydata)`. Likewise on the server side, events are propagated to `Network_*` method callbacks and data is sent back to clients with the `client.Send(mydata)` method.

The [PodSixNet mailing list](http://groups.google.com/group/podsixnet) is good for getting help from other users.

For users of the Construct game making environment for Windows, there is a tutorial on doing multiplayer networking with PodSixNet, [here](http://www.scirra.com/forum/viewtopic.php?f=8&t=6299). Thanks to Dave Chabo for contributing this tutorial.

Here is [another tutorial by Julian Meyer](http://www.raywenderlich.com/38732/multiplayer-game-programming-for-teens-with-python).

Install
-------

First make sure you have [Python](http://python.org/) 2.4 or greater installed.

Next you'll want to get the PodSixNet source.

The module is found inside a subdirectory called PodSixNet within the top level folder. There's an `__init__.py` inside there, so you can just copy or symlink the PodSixNet sub-directory into your own project and then do `import PodSixNet`, or else you can run `sudo setup.py install` to install PodSixNet into your Python path. Use `sudo setup.py develop` if you want to stay up to date with the cutting edge and still be able to svn/bzr up every now and then.

By default PodSixNet uses a binary encoder to transfer data over the network, but it can optionally use the [JSON](http://json.org/) format or other formats supported by a serialiser which has 'dumps' and 'loads' methods. If you want to serialise your data using JSON you can change the first line of Channel.py to 'from simplejson import dumps, loads' or use the built-in json library in Python 2.6 or higher. This will allow you to write game clients in languages that can't read the 'rencode' binary format, such as Javascript.

Examples
--------

Chat example:

 * `python examples/ChatServer.py`
 * and a couple of instances of `python examples/ChatClient.py`

Whiteboard example:

 * `python examples/WhiteboardServer.py`
 * and a couple of instances of `python examples/WhiteboardServer.py`

LagTime example (measures round-trip time from the server to the client):

 * `python examples/LagTimeServer.py`
 * and a couple of instances of `python examples/LatTimeClient.py`

Quick start - Server
--------------------

You will need to subclass two classes in order to make your own server. Each time a client connects, a new Channel based class will be created, so you should subclass Channel to make your own server-representation-of-a-client class like this:

	from PodSixNet.Channel import Channel
	
	class ClientChannel(Channel):
	
		def Network(data):
			print data
		
		def Network_myaction(data):
			print "myaction:", data

Whenever the client does `connection.Send(mydata)`, the `Network()` method will be called. The method `Network_myaction()` will only be called if your data has a key called 'action' with a value of "myaction". In other words if it looks something like this:

	data = {"action": "myaction", "blah": 123, ... }

Next you need to subclass the Server class like this:

	from PodSixNet.Server import Server
	
	class MyServer(Server):
		
		channelClass = ClientChannel
		
		def Connected(self, channel, addr):
			print 'new connection:', channel

Set `channelClass` to the channel class that you created above. The method `Connected()` will be called whenever a new client connects to your server. See the example servers for an idea of what you might do each time a client connects. You need to call `Server.Pump()` every now and then, probably once per game loop. For example:

	myserver = MyServer()
	while True:
		myserver.Pump()
		sleep(0.0001)

When you want to send data to a specific client/channel, use the Send method of the Channel class:

	channel.Send({"action": "hello", "message": "hello client!"})

Quick start - Client
--------------------

To have a client connect to your new server, you should use the Connection module. See `pydoc Connection` for more details, but here's a summary:

`Connection.connection` is a singleton Channel which connects to the server. You'll only have one of these in your game code, and you'll use it to connect to the server and send messages to the server.

	from Connection import connection
	
	# connect to the server - optionally pass hostname and port like: ("mccormick.cx", 31425)
	connection.Connect()
	
	connection.Send({"action": "myaction", "blah": 123, "things": [3, 4, 3, 4, 7]})

You'll also need to put the following code once somewhere in your game loop:

	connection.Pump()

Any time you have an object in your game which you want to receive messages from the server, subclass `ConnectionListener`. For example:

	from Connection import ConnectionListener
	
	class MyNetworkListener(ConnectionListener):
	
		def Network(self, data):
			print 'network data:', data
		
		def Network_connected(self, data):
			print "connected to the server"
		
		def Network_error(self, data):
			print "error:", data['error'][1]
		
		def Network_disconnected(self, data):
			print "disconnected from the server"
		
		def Network_myaction(data):
			print "myaction:", data

Just like in the server case, the network events are received by `Network_*` callback methods, where you should replace '*' with the value in the 'action' key you want to catch. You can implement as many or as few of the above as you like. For example, NetworkGUI would probably only want to listen for the `_connected`, `_disconnected`, and `_error` network events. The data for `_error` always comes in the form of network exceptions, like (111, 'Connection refused') - these are passed straight from the socket layer and are standard socket errors.

Another class might implement custom methods like `Network_myaction()`, which will receive any data that gets sent from the server with an 'action' key that has the name 'myaction'. For example, the server might send a message with the number of players currently connected like so:

	channel.Send({"action": "numplayers", "players": 10})

And the listener would look like this:

	from Connection import ConnectionListener
	
	class MyPlayerListener(ConnectionListener):
	
		def Network_numplayers(data):
			# update gui element displaying the number of currently connected players
			print data['players']

You can subclass `ConnectionListener` as many times as you like in your application, and every class you make which subclasses it will receive the network events via named Network callbacks. You should call the `Pump()` method on each object you instantiate once per game loop:

	gui = MyPlayerListener()
	while 1:
		connection.Pump()
		gui.Pump()

License
-------

Copyright [Chris McCormick](http://mccormick.cx/), 2009-2015.

PodSixNet is licensed under the terms of the LGPL v3.0 or higher. See the file called [COPYING](COPYING) for details.

This basically means that you can use it in most types of projects (commercial or otherwise), but if you make changes to the PodSixNet code you must make the modified code available with the distribution of your software. Hopefully you'll tell us about it so we can incorporate your changes. I am not a lawyer, so please read the license carefully to understand your rights with respect to this code.

Why not use Twisted instead?
---------------------------

Twisted is a fantastic library for writing robust network code. I have used it in several projects in the past, and it was quite nice to work with. That said, Twisted:

* wants to steal the mainloop
* is bloated not KISS (it implements many many different protocols)
* has a weird template launching language when Python should do just fine
* is not written 100% for the specfic use-case of multiplayer games

These are some of the reasons why I decided to write a library that is lightweight, has no dependencies except Python, and is dedicated 100% to the task of multiplayer game networking.

