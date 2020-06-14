from __future__ import print_function
import sys

from PodSixNet.asyncwrapper import asynchat
from PodSixNet.rencode import loads, dumps

class Channel:
    endchars = '\0---\0'
    def __init__(self, conn=None, addr=(), server=None, map=None):
        self.async_chat = asynchat.async_chat(getattr(conn, "socket", conn), map)
        # since async_chat requires some methods to be implemented, we'll override them by assigning our own
        self.async_chat.collect_incoming_data = self.collect_incoming_data
        self.async_chat.found_terminator = self.found_terminator
        self.addr = addr
        self._server = server
        self._ibuffer = b""
        self.set_terminator(self.endchars.encode())
        self.sendqueue = []
    
    @property
    def terminator(self):
        """just a convenient property that returns the async_chat's terminator"""
        return self.async_chat.terminator

    @property
    def socket(self):
        return self.async_chat.socket

    @socket.setter
    def socket(self, value):
        self.async_chat.socket = value

    def connect(self, addr):
        """calls the connect function that the async_chat instance has inherited"""
        return self.async_chat.connect(addr)

    def collect_incoming_data(self, data):
        self._ibuffer += data
    
    def found_terminator(self):
        data = loads(self._ibuffer)
        self._ibuffer = b""
        
        if type(dict()) == type(data) and 'action' in data:
            [getattr(self, n)(data) for n in ('Network_' + data['action'], 'Network') if hasattr(self, n)]
        else:
            print("OOB data:", data)

    def set_terminator(self, term):
        """calls the set_terminator on the async_chat instance """
        return self.async_chat.set_terminator(term)
    
    def get_terminator(self):
        """return the channel's terminator  from the async_chat instance"""
        return self.async_chat.get_terminator()

    def create_socket(self, *args, **kwargs):
        """creates a socket from the async_chat instance"""
        return self.async_chat.create_socket(*args, **kwargs)

    def pump(self):
        [self.async_chat.push(d) for d in self.sendqueue]
        self.sendqueue = []
    
    def send(self, data):
        """Returns the number of bytes sent after enoding."""
        outgoing = dumps(data) + self.endchars.encode()
        self.sendqueue.append(outgoing)
        return len(outgoing)
    
    def handle_connect(self):
        if hasattr(self, "Connected"):
            self.connected()
        else:
            print("Unhandled Connected()")
    
    def handle_error(self):
        try:
            self.async_chat.close()
        except:
            pass
        if hasattr(self, "error"):
            self.error(sys.exc_info()[1])
        else:
            self.async_chat.handle_error(self)
    
    def handle_expt(self):
        pass
    
    def handle_close(self):
        if hasattr(self, "close"):
            self.close()
        self.async_chat.handle_close(self)
