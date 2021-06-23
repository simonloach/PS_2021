import logging
import socket
import sys
import threading
import time

from player import Player, PlayerState
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
        except socket.error:
            logging.info('Failed')
            sys.exit()

        self.socket.listen(5)
        logging.info('Listening')

    def connect(self, client_socket):
        try:
            this_player = Player(client_socket)
            self.players.append(this_player)
            client_socket.send(b"0")
            while True:
                if this_player.state == PlayerState.DISCONNECTED:
                    #TODO create self.players mutex
                    if len(self.players)>1:
                        logging.info("Starting game")
                        _ = self.players.pop(self.players.index(this_player))
                        other_player = self.players.pop(0)
                        self.games.append(Game(this_player, other_player))
                        this_player.send_msg(b"1")
                        other_player.send_msg(b"1")
                    else:
                        time.sleep(0.5)
                elif this_player.state == PlayerState.IN_GAME:
                    if this_player.game.is_now_my_turn(this_player):
                        this_player.send_msg(b"2")
                        this_player.wait_for_input()
                        # new move
                        this_player.game.move(move)
                    else:
                        time.sleep(0.5)

        except Exception as e:
            logging.error(e)

    def accept(self):
        clientSocket, addr = self.socket.accept()
        logging.info('Accepted')
        t=threading.Thread(target=Server.connect, args=(self, clientSocket))
        t.start()
        logging.info('Threaded')


x=Server()
while True:
    logging.info('Accept')
    x.accept()
