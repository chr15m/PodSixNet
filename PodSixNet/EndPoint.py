# coding=utf-8
import socket

from PodSixNet.asyncwrapper import poll
from PodSixNet.Channel import Channel

class EndPoint(Channel):
    """
    The endpoint queues up all network events for other classes to read.
    """
    def __init__(self, address=("127.0.0.1", 31425), map=None):
        self.address = address
        self.isConnected = False
        self.queue = []
        if map is None:
            self._map = {}
        else:
            self._map = map
    
    def DoConnect(self, address=None):
        if address:
            self.address = address
        try:
            Channel.__init__(self, map=self._map)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.connect(self.address)
        except socket.gaierror as e:
            self.queue.append({"action": "error", "error": e.args})
        except socket.error as e:
            self.queue.append({"action": "error", "error": e.args})
    
    def GetQueue(self):
        return self.queue
    
    def Pump(self):
        Channel.Pump(self)
        self.queue = []
        poll(map=self._map)
    
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
 
