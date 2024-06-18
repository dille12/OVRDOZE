import socket
import json
from functools import wraps

# Dummy server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5555

# Dummy player class representing a player in the game
class Player:
    def __init__(self, player_id, x, y):
        self.id = player_id
        self.x = x
        self.y = y

# Dummy server class to simulate server functionality
class Server:
    def __init__(self):
        self.players = {}

    def handle_movement(self, player_id, x, y):
        self.players[player_id].x = x
        self.players[player_id].y = y
        self.broadcast_update()

    def broadcast_update(self):
        # Simulate broadcasting updates to all connected clients
        pass

# Dummy client class to simulate client functionality
class Client:
    def __init__(self):
        self.player = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    def send_data(self, data):
        encoded_data = json.dumps(data).encode('utf-8')
        self.server_socket.sendall(encoded_data)

# Decorator for synchronizing player movement
def synchronize_movement(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Call the original function
        func(self, *args, **kwargs)
        # Package data and send to server
        data = {
            'player_id': self.player.id,
            'x': self.player.x,
            'y': self.player.y
        }
        self.send_data(data)
    return wrapper

# Example usage of the decorators
class Game:
    def __init__(self):
        self.server = Server()
        self.client = Client()
        # Simulate player creation
        self.client.player = Player(player_id=1, x=0, y=0)
        self.server.players[1] = self.client.player

    @synchronize_movement
    def move_player(self, x, y):
        self.client.player.x = x
        self.client.player.y = y
        self.server.handle_movement(self.client.player.id, x, y)

# Example usage of the game
if __name__ == "__main__":
    game = Game()
    # Simulate player movement
    game.move_player(1, 1)
