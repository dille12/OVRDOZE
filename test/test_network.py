import unittest
from network import *
import threading
from time import sleep
from _socketEchoServer import socketEchoServerMock

class TestNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("cleaning up class")
        self.network=None;
        self.est=None;
    @classmethod
    def tearDownClass(self):
        print("tear down\n\n\n");
        print(self.network,"is network");
        print(self.est,"is est")
        print("tear down down\n\n\n")
        self.network=None;
        self.est=None;
        sleep(5)
    
    def getMockEchoServer(self,autoReply=False):
            # echo server..
            es = socketEchoServerMock()
            est = threading.Thread(target=es.threaded_test_server,
                                   kwargs={'autoReply': autoReply})
            est.daemon = True
            est.start()
            return est
            
    def test_connect(self):
        self.est=self.startMockEchoServer(autoReply=True)
        self.network = Network('127.0.0.1') 
        assert self.network.client._closed == False
        self.network.client.close()
        assert self.network.client._closed == True
    async def test_send(self):
        print('entered: test_send')
        self.est=self.startMockEchoServer()
        self.network = Network('127.0.0.1')
        # test send 
        ret = await self.network.send("test_str")
        assert ret == "test_str"
        ret = await self.network.send("shutdown_server")
        # test send w/ socket _closed
        # expect network.send to return "KILL"
        self.network.client.close()
        ret = await self.network.send("test_str")
        assert ret == "KILL"
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
