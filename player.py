"""Player class"""

from enum import Enum

class PlayerState(Enum):
    DISCONNECTED = 0
    IN_GAME = 1

class Player:
    def __init__(self, socket):
        self.socket = socket
        self.state = PlayerState.DISCONNECTED

    def start_game(self, game):
        self.game = game
        self.state = PlayerState.IN_GAME

    def send_msg(self, msg):
        self.socket.send(msg)

    def wait_for_input(self):
        self.socket.recv(1024)