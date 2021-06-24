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
    """A server that handles all Client() instances and hosts games

    Attributes:
        players: List<Player>       List of Player objects
        games: List<Game>          List of Game objects
        socket: socket.Socket()     Socket for communicating with Client() instances


    Methods:
        connect(client_socket: socket.Socket())  Updates self.board basing on bytearray received from Server()
        accept()    Accepts new connections comming from Client() instances.
                    Start thread for each Client with connect(clientSocket)
    """
    def __init__(self):
        self.players = list()
        self.games = list()
        self.players_lock = threading.Lock()
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
                    self.players_lock.acquire()
                    if len(self.players)>1:
                        _ = self.players.pop(self.players.index(this_player))
                        other_player = self.players.pop(0)
                        self.players_lock.release()
                        g = Game(this_player, other_player)
                        self.games.append(g)
                        this_player.send_msg(MessageType.NEW_GAME, b'\x01')
                        other_player.send_msg(MessageType.NEW_GAME, b'\x02')
                        g.start()
                    else:
                        self.players_lock.release()
                        time.sleep(0.5)

                elif this_player.state == PlayerState.FINISHED:
                    this_player.state = PlayerState.DISCONNECTED
                    self.players_lock.acquire()
                    self.players.append(this_player)
                    self.players_lock.release()

                else:
                    if this_player.game.is_now_my_turn(this_player):
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

    def main_loop(self):
        while True:
            self.accept()


if __name__ == '__main__':
    Server().main_loop()
