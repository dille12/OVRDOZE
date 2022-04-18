import socket
import sys


port = 5555


class Network:



    def __init__(self, ip_address):

        print("Network init:")
        print("ip:",ip_address)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip_address # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = port
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            print("SOCKET ERROR:",e)
            sys.exit()
            return "KILL"
