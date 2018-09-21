from __future__ import print_function
import socket

from PodSixNet.asyncwrapper import poll, asyncore
from PodSixNet.Channel import Channel

class Server(asyncore.dispatcher):
    channelClass = Channel
    
    def __init__(self, channelClass=None, localaddr=("127.0.0.1", 5071), listeners=5):
        if channelClass:
            self.channelClass = channelClass
        self._map = {}
        self.channels = []
        asyncore.dispatcher.__init__(self, map=self._map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr()
        self.bind(localaddr)
        self.listen(listeners)
    
    def handle_accept(self):
        try:
            conn, addr = self.accept()
        except socket.error:
            print('warning: server accept() threw an exception')
            return
        except TypeError:
            print('warning: server accept() threw EWOULDBLOCK')
            return
        print("connection")
        self.channels.append(self.channelClass(conn, addr, self, self._map))
        self.channels[-1].Send({"action": "connected"})
        if hasattr(self, "Connected"):
            self.Connected(self.channels[-1], addr)
    
    def Pump(self):
        [c.Pump() for c in self.channels]
        poll(map=self._map)

