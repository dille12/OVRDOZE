import unittest
import threading
import os,sys
from server import *
from network import *
# cwd = os.getcwd();
# sys.path.append(f'{cwd}/test')
from _socketEchoServer import socketEchoServerMock

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.est=None;
        print("setting up class",cls)
        try:
           print("trying");
           cls.startActualServer()
        except Exception as e:
            print("tearing down due to error: ",e)
            cls.tearDownClass()
            raise
    @classmethod    
    def startActualServer(cls):
        print('startActualServer')
        cls.est = threading.Thread(target=server_run)

        cls.est.daemon = True
        cls.est.start()
        print("server started")
         # to still mark the test as failed.
    def test_threaded_client(cls):
        print('test_threaded_client')
        pass
    def test_return_players(cls):
        print('test_return_players')
  
        ret = return_players()
        assert ret == {}
    def test_server_run(cls):
        print('test_server_run')
        pass # only for now
        print('a')
        cls.startActualServer()
        print('b')
        hostname = socket.gethostname()
        net = Network(socket.gethostbyname(hostname))
        assert net.client._closed == False
        ret = net.send("test_str")
        net.client.close()
        assert net.client._closed == True
        assert net.id == 'ok' # locking current behavior w/ test
                              # even if i don't fully understand :p
        net = Network(socket.gethostbyname(hostname))
        assert net.client._closed == False
        net.client.close()
        assert net.client._closed == True
        # connect
        del net
        # should get 'ok'
        #send empty data to close?'''
