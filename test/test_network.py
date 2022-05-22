import unittest
from network import *
import threading

from test._socketEchoServer import socketEchoServerMock

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
        self.startMockEchoServer(autoReply=True)
        net = Network('127.0.0.1')
        assert net.client._closed == False
        net.client.close()
        assert net.client._closed == True
    def test_send(self):
        print('entered: test_send')
        self.startMockEchoServer()
        net = Network('127.0.0.1')
        ret = net.send("test_str")
        assert ret == "test_str"
        ret = net.send("shutdown_server")
        net.client.close()
    # 
    # def test_send_with_dead_con(self):
    #     print('entered: test_send_with_dead_con')
    #     self.startMockEchoServer()
    #     print('....')
    #     net = Network('127.0.0.1')
    #     print('close..')
    #     net.client.close()
    #     print('sending')
    #     ret = net.send("test_str")
    #     assert ret == "KILL"
