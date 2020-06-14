from __future__ import print_function

from time import sleep, localtime
from weakref import WeakKeyDictionary
from time import time
import sys

from PodSixNet.server import Server
from PodSixNet.channel import Channel

class LagTimeChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.count = 0
        self.times = []
    
    def close(self):
        print(self, 'Client disconnected')
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_ping(self, data):
        print(self, "ping %d round trip time was %f" % (data["count"], time() - self.times[data["count"]]))
        self.Ping()
    
    def Ping(self):
        print(self, "Ping:", self.count)
        self.times.append(time())
        self.send({"action": "ping", "count": self.count})
        self.count += 1

class LagTimeServer(Server):
    channel_class = LagTimeChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print('Server launched')
    
    def connected(self, channel, addr):
        print(channel, "Channel connected")
        channel.Ping()
    
    def Launch(self):
        while True:
            self.pump()
            sleep(0.0001)

# get command line argument of server, port
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        s = LagTimeServer(localaddr=(host, int(port)))
        s.Launch()

