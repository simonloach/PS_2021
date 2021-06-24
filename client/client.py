from utils.definitions import MessageType
from communicator import Communicator, Message
from board import Board

import socket
import random
import argparse
import re
import logging
import sys
from queue import Queue
import threading

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename='client.log', encoding='utf-8', level=logging.DEBUG, format=format, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description='Client for Tic Tac Toe game written by: \n\t Szymon Piskorz \n\tLukasz Sroka\n\tJaroslaw Zelechowski')
parser.add_argument('-4',metavar="X.X.X.X",help='IPv4 Address', type=str)
parser.add_argument('-6',metavar="Y:Y:Y:Y:Y:Y:Y:Y",help='IPv6 Address', type=str)
parser.add_argument('-p',metavar="{0..65535}", help="Port number for the server", type=str)
parser.add_argument('-a',help="Enable automatic mover", action="store_true", default=False)
args = parser.parse_args()


IP_V4_REGEX = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
IP_V6_REGEX = re.compile('^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)$')
PORT_REGEX = re.compile('^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')

def parse_args(**kwargs):

    if kwargs['p'] is not None:
        if PORT_REGEX.match(kwargs['p']):
            port = kwargs['p']
    else:
        raise Exception("Port is incorrect")

    if kwargs['4'] is not None and kwargs['6'] is not None:
        raise Exception('Two addresses for the server were provided, both IPv4 and IPv6')
    elif kwargs['4'] is not None:
        if IP_V4_REGEX.match(kwargs['4']):
            ip_type = socket.AF_INET
            ip_addr = kwargs['4']
        else:
            raise Exception('Regex for IPv4 address failed match.')
    elif kwargs['6'] is not None:
        if IP_V6_REGEX.match(kwargs['6']):
            ip_type = socket.AF_INET6
            ip_addr = kwargs['6']
        else:
            raise Exception('Regex for IPv6 address failed match.')
    else:
        raise Exception('No address for the server was provided.')

    config = {"ip_type": ip_type, "ip_addr": ip_addr, "port": port, "automover": kwargs["a"] }
    logging.debug(f"Staring client with config: {config}")
    return config

class Client:

    def __init__(self, config):
        self.comm = Communicator(config)
        self.config = config
        self.board:Board = Board()
        self.in_msg_queue = Queue()
        self.out_msg_queue = Queue()
        self.last_move = (None, None)
        self.cursor=None

    def connect(self):
        self.comm.connect()

    def get_users_move(self):
        '''
            x, y are strings represendation of int from range(1,3)
        '''
        if self.config["automover"]:
            x = chr(random.randint(0, 2) + ord('1'))
            y = chr(random.randint(0, 2) + ord('1'))
        else:
            x=input("Provide X coordinate:\t")
            y=input("Provide Y coordinate:\t")
        self.last_move = (x, y)
        return (x, y)

    def main_loop(self):
        while True:
            msg = self.in_msg_queue.get()

            if msg.type == MessageType.CONNECTED:
                self.board.add_message("You're connected to the server")
                self.board.add_message("Waiting for the opponent")
                print(self.board)
            elif msg.type == MessageType.NEW_GAME:
                self.cursor = msg.payload
                self.board.clear()
                self.board.add_message("Good Luck.")
                if self.cursor == 2:
                    self.board.add_message("Opponent's turn now.")
                    print(self.board)
            elif msg.type == MessageType.YOUR_TURN:
                self.board.add_message("Now it's your turn!")
                print(self.board)
                (x, y) = self.get_users_move()
                move_msg = Message(MessageType.NEXT_MOVE, (x, y))
                self.out_msg_queue.put(move_msg)
            elif msg.type == MessageType.MOVE_VALIDITY:
                if bool(msg.payload):
                    self.board.update_board_with_local(self.last_move, self.cursor)
                    self.board.add_message("Opponent's turn now.")
                    print(self.board)
                else:
                    self.board.add_message("Invalid move")
                    print(self.board)
                    (x, y) = self.get_users_move()
                    move_msg = Message(MessageType.NEXT_MOVE, (x, y))
                    self.out_msg_queue.put(move_msg)
            elif msg.type == MessageType.BOARD_UPDATE:
                self.board.update_board(msg.payload)
                print(self.board)

    def in_msg_thread_func(self):
        try:
            while True:
                new_msg = self.comm.next_msg()
                self.in_msg_queue.put(new_msg)
        except Exception as e:
            logging.exception("exception in in_msg_thread function")

    def out_msg_thread_func(self):
        try:
            while True:
                msg = self.out_msg_queue.get()
                self.comm.send_msg(msg)
        except Exception as e:
            logging.exception("exception in out_msg_thread function")

if __name__ == '__main__':
    try:
        config = parse_args(**vars(args))
    except Exception as e:
        print(e)
        sys.exit(1)

    client = Client(config)

    try:
        client.connect();
        in_msg_thread = threading.Thread(target=client.in_msg_thread_func)
        in_msg_thread.start()
        out_msg_thread = threading.Thread(target=client.out_msg_thread_func)
        out_msg_thread.start()

        client.main_loop()
    except TimeoutError as e:
        logging.error("Connection timed out!")
    except Exception as e:
        logging.exception("Other exception")
    except KeyboardInterrupt:
        logging.info("Program stopped by Ctrl-C")
    finally:
        logging.info("Program finished")

    sys.exit(0)
