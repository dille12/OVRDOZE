import socket
# from _thread import *
import threading

class socketEchoServerMock :
    def __init__(self):
        pass

    def threaded_test_server(self,autoReply=False):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 5555  # Port to listen on (non-privileged ports are > 1023)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = b"testStr"
                conn.sendall(data)
                while True:
                    if not autoReply:
                        data = conn.recv(1024)
                        if data:
                            if data == 'shutdown_server':
                                break
                            conn.sendall(data)
                    else:
                        data = b"testStr"
                        conn.sendall(data)
                        break

    def startMockEchoServer(self,autoReply=False):
            print(f"Starting threaded_test_server. autoreply: {autoReply}")
            self.eg = threading.Thread(target=self.threaded_test_server,args=(autoReply))
            self.eg.start()


    def startTestClient(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 5555  # The port used by the server
        print("Starting startTestClient")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

        print(f"Received {data!r}")
