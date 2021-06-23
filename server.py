import logging
import socket
import sys
import threading
import time

from player import MessageType, Player, PlayerState
from game import Game

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

class Server:
    def __init__(self):
        self.players = list()
        self.games = list()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', 2137))
        except socket.error as e:
            logging.error(f'Failed with socker error {e}')
            sys.exit()

        self.socket.listen(5)
        logging.info('Listening')

    def connect(self, client_socket):
        try:
            this_player = Player(client_socket)
            self.players.append(this_player)
            this_player.send_msg(MessageType.CONNECTED)
            while True:
                if this_player.state == PlayerState.DISCONNECTED:
                    #TODO create self.players mutex
                    if len(self.players)>1:
                        logging.info("Starting game")
                        _ = self.players.pop(self.players.index(this_player))
                        other_player = self.players.pop(0)
                        self.games.append(Game(this_player, other_player))
                        this_player.send_msg(MessageType.NEW_GAME)
                        other_player.send_msg(MessageType.NEW_GAME)
                    else:
                        time.sleep(0.5)
                else:
                    if this_player.game.is_now_my_turn(this_player):
                        this_player.send_msg(MessageType.YOUR_TURN)
                        move = this_player.wait_for_move()
                        validity = this_player.game.move(move)
                        this_player.send_msg(MessageType.MOVE_VALIDITY, validity.to_bytes(1, 'big'))
                    else:
                        time.sleep(0.5)

        except Exception as e:
            logging.exception("Exception during client handling")

    def accept(self):
        clientSocket, addr = self.socket.accept()
        logging.info('Accepted new client')
        t = threading.Thread(target=Server.connect, args=(self, clientSocket))
        t.start()


x=Server()
while True:
    x.accept()
