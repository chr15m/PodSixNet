# coding=utf-8
from __future__ import print_function

import unittest
import sys
from time import sleep, time
import socket

from PodSixNet.asyncwrapper import poll, asyncore
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.EndPoint import EndPoint

class FailEndPointTestCase(unittest.TestCase):
    def setUp(self):
        
        class FailEndPoint(EndPoint):
            def __init__(self):
                EndPoint.__init__(self, ("localhost", 31429))
                self.result = ""
            
            def Error(self, error):
                self.result = error
            
            def Test(self):
                self.DoConnect()
                start = time()
                while not self.result and time() - start < 10:
                    self.Pump()
                    sleep(0.001)
        
        self.endpoint_bad = FailEndPoint()
    
    def runTest(self):
        self.endpoint_bad.Test()
        want = "[Errno 111] Connection refused"
        self.assertEqual(str(self.endpoint_bad.result), str(want), "Socket got %s instead of %s" % (str(self.endpoint_bad.result), str(want)))
    
    def tearDown(self):
        del self.endpoint_bad

class EndPointTestCase(unittest.TestCase):
    def setUp(self):
        self.outgoing = [
            {"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}},
            {"action": "hello", "data": [454, 35, 43, 543, "aabv"]},
            {"action": "hello", "data": [10] * 512},
            #{"action": "hello", "data": [10] * 512, "otherstuff": "hello\0---\0goodbye", "x": [0, "---", 0], "y": "zÃ¤Ã¶"},
        ]
        self.count = len(self.outgoing)
        self.lengths = [len(data['data']) for data in self.outgoing]
        
        
        class ServerChannel(Channel):
            def Network_hello(self, data):
                self._server.received.append(data)
                self._server.count += 1
                self.Send({"action": "gotit", "data": "Yeah, we got it: " + str(len(data['data'])) + " elements"})
        
        class TestEndPoint(EndPoint):
            received = []
            connected = False
            count = 0
            
            def Network_connected(self, data):
                self.connected = True
            
            def Network_gotit(self, data):
                self.received.append(data)
                self.count += 1
                
        
        class TestServer(Server):
            connected = False
            received = []
            count = 0
            
            def Connected(self, channel, addr):
                self.connected = True
        
        self.server = TestServer(channelClass=ServerChannel, localaddr=("127.0.0.1", 31426))
        self.endpoint = TestEndPoint(("127.0.0.1", 31426))
    
    def runTest(self):
        self.endpoint.DoConnect()
        for o in self.outgoing:
            self.endpoint.Send(o)
        
        
        for x in range(50):
            self.server.Pump()
            self.endpoint.Pump()
            
            # see if what we receive from the server is what we expect
            for r in self.server.received:
                self.failUnless(r == self.outgoing.pop(0))
            self.server.received = []
            
            # see if what we receive from the client is what we expect
            for r in self.endpoint.received:
                self.failUnless(r['data'] == "Yeah, we got it: %d elements" % self.lengths.pop(0))
            self.endpoint.received = []
            
            sleep(0.001)
        
        self.assertTrue(self.server.connected, "Server is not connected")
        self.assertTrue(self.endpoint.connected, "Endpoint is not connected")
        
        self.failUnless(self.server.count == self.count, "Didn't receive the right number of messages")
        self.failUnless(self.endpoint.count == self.count, "Didn't receive the right number of messages")
        
        self.endpoint.Close()
        
    
    def tearDown(self):
        del self.server
        del self.endpoint

class ServerTestCase(unittest.TestCase):
    testdata = {"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}}
    def setUp(self):
        print("ServerTestCase")
        print("--------------")
        
        class ServerChannel(Channel):
            def Network_hello(self, data):
                print("*Server* ran test method for 'hello' action")
                print("*Server* received:", data)
                self._server.received = data
        
        class EndPointChannel(Channel):
            connected = False
            def Connected(self):
                print("*EndPoint* Connected()")
            
            def Network_connected(self, data):
                self.connected = True
                print("*EndPoint* Network_connected(", data, ")")
                print("*EndPoint* initiating send")
                self.Send(ServerTestCase.testdata)
        
        class TestServer(Server):
            connected = False
            received = None
            def Connected(self, channel, addr):
                self.connected = True
                print("*Server* Connected() ", channel, "connected on", addr)
        
        self.server = TestServer(channelClass=ServerChannel, localaddr=("127.0.0.1", 31427))
        
        sender = asyncore.dispatcher(map=self.server._map)
        sender.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect(("127.0.0.1", 31427))
        self.outgoing = EndPointChannel(sender, map=self.server._map)
        
    def runTest(self):
        from time import sleep
        print("*** polling for half a second")
        for x in range(250):
            self.server.Pump()
            self.outgoing.Pump()
            if self.server.received:
                self.failUnless(self.server.received == self.testdata)
                self.server.received = None
            sleep(0.001)
        self.failUnless(self.server.connected == True, "Server is not connected")
        self.failUnless(self.outgoing.connected == True, "Outgoing socket is not connected")
    
    def tearDown(self):
        pass
        del self.server
        del self.outgoing


if __name__ == "__main__":
    unittest.main()

