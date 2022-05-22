import unittest
from network import *
import threading
from _socketEchoServer import socketEchoServerMock

class TestNetwork(unittest.TestCase):

    def startMockEchoServer(self,autoReply=False):
            # echo server..
            es = socketEchoServerMock()
            est = threading.Thread(target=es.threaded_test_server,
                                   kwargs={'autoReply': autoReply})
            est.daemon = True
            est.start()
            self.est = est

    def test_connect(self):
        # test test_connect
        # however Newwork.init expect connecting client to send
        # data ... mock server has a flag to get around this,
        # without having to include network.send in this test
        self.startMockEchoServer(autoReply=True)
        net = Network('127.0.0.1')
        assert net.client._closed == False
        net.client.close()
        assert net.client._closed == True
    def test_send(self):
        print('entered: test_send')
        self.startMockEchoServer()
        net = Network('127.0.0.1')
        # test send
        ret = net.send("test_str")
        assert ret == "test_str"
        ret = net.send("shutdown_server")
        # test send w/ socket _closed - forcing socket error exception
        # expect network.send to return "KILL"
        net.client.close()
        ret = net.send("test_str")
        assert ret == "KILL"
