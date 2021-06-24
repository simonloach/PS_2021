from player import MessageType
from board import Board

import socket
import argparse
import re
import logging
import os

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG, format=format, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description='Client for Tic Tac Toe game written by: \n\t Szymon Piskorz \n\tLukasz Sroka\n\tJaroslaw Zelechowski')
parser.add_argument('-4',metavar="X.X.X.X",help='IPv4 Address', type=str)
parser.add_argument('-6',metavar="Y:Y:Y:Y:Y:Y:Y:Y",help='IPv6 Address', type=str)
parser.add_argument('-p',metavar="{0..65535}", help="Port number for the server", type=str)
args = parser.parse_args()


IP_V4_REGEX = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
IP_V6_REGEX = re.compile('^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)$')
PORT_REGEX = re.compile('^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')

class Client:

    def __init__(self, **kwargs):
        self.last_move = (None, None)
        if kwargs['p'] is not None:
            if PORT_REGEX.match(kwargs['p']):
                self.port = kwargs['p']
                logging.debug(f"Instantiated port")
        else:
            raise Exception("Port is incorrect")

        if kwargs['4'] is not None and kwargs['6'] is not None:
            raise Exception('Two addresses for the server were provided, both IPv4 and IPv6')
        elif kwargs['4'] is not None:
            if IP_V4_REGEX.match(kwargs['4']):
                self.server_address = kwargs['4']
                logging.debug(f"Instantiated IPv4 address")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logging.debug(f"Instantiated IPv4 socket")
            else:
                raise Exception('Regex for IPv4 address failed match.')
        elif kwargs['6'] is not None:
            if IP_V6_REGEX.match(kwargs['6']):
                self.server_address = kwargs['6']
                logging.debug(f"Instantiated IPv6 address")
                self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                logging.debug(f"Instantiated IPv6 socket")
            else:
                raise Exception('Regex for IPv6 address failed match.')
        else:
            raise Exception('No address for the server was provided.')

        self.board=Board()
        self.cursor=None
        self.buffer=bytes()


    def connect(self):
        logging.info(f"Connecting to {self.server_address} on port {self.port}")
        self.socket.connect((self.server_address, int(self.port)))
        logging.info(f"Connected!")
    

    def listen(self):
        logging.info(f"Listening")
        message = self.socket.recv(10)
        return message


    def send_move(self):
        '''
            x, y are strings represendation of int from range(0,2)
        '''
        x=input("Provide X coordinate:\t")
        y=input("Provide Y coordinate:\t")
        self.set_last(x, y)
        self.socket.send(MessageType.NEXT_MOVE.value.to_bytes(1, "big") + x.encode() + y.encode() )
        return self
    

    def set_last(self, x, y):
        self.last_move = (x,y)


    def get_last(self):
        return self.last_move


    def play(self):
        try:
            if not c.buffer:
                c.buffer += c.listen()
                
            else:
                message_id = c.buffer[0]

                if message_id == MessageType.CONNECTED.value:
                    c.buffer = c.buffer[1:]
                    c.board.add_message("Waiting for opponent.")

                elif message_id == MessageType.NEW_GAME.value:
                    c.board.clear_board()
                    message_payload = c.buffer[1]
                    c.cursor = message_payload
                    c.buffer = c.buffer[2:]
                    if c.cursor == 2:
                        c.board.add_message("Opponents turn!")

                elif message_id == MessageType.YOUR_TURN.value:
                    c.board.add_message("Your turn!")
                    print(c.board)
                    c.send_move()
                    c.buffer = c.buffer[1:]

                elif message_id == MessageType.MOVE_VALIDITY.value:
                    message_payload = c.buffer[1]
                    if bool(message_payload):
                        c.board.update_board_with_local(c.get_last(), c.cursor)
                        c.board.add_message("Opponents turn!")
                    else:
                        c.board.add_message("Invalid move!")
                        print(c.board)
                        logging.info("Bad move!")
                        c.send_move()
                    c.buffer = c.buffer[2:]

                elif message_id == MessageType.BOARD_UPDATE.value:
                    message_payload = c.buffer[1:10]
                    c.board.update_board(message_payload)
                    c.buffer = c.buffer[10:]
            print(c.board)
        except IndexError:
            c.buffer.append(c.listen())

if __name__ == '__main__':
    try:
        c = Client(**vars(args))
        c.connect()
        while True:
            c.play()

    except TimeoutError as e:
        logging.error("Connection timed out!")
    except Exception as e:
        logging.error("Parsing parameters encountered error: \n\t", e)
    finally:
        logging.info("Program finished")
        


    
