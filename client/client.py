from utils.definitions import MessageType
from communicator import Communicator, ConnectionConfig
from board import Board

import socket
import argparse
import re
import logging
import sys
import time
from queue import Queue
import threading

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

    config = ConnectionConfig(ip_type, ip_addr, port)
    logging.debug(f"Staring client with config: {config}")
    return config

class Client:

    def __init__(self, **kwargs):
        self.last_move = (None, None)

        self.board=Board()
        self.cursor=None
        self.msg_queue = Queue()

    def send_move(self):
        '''
            x, y are strings represendation of int from range(0,2)
        '''
        x=input("Provide X coordinate:\t")
        y=input("Provide Y coordinate:\t")
        self.set_last(x, y)
        return self

    def main_loop(self):
        while True:
            msg = self.msg_queue.get()
            print(msg)

            if msg[0] == MessageType.CONNECTED:
                self.board.add_message("You're connected to the server")
                print(self.board)

    def msg_thread_func(self):
        try:
            comm = Communicator(config)
            comm.connect()
            while True:
                new_msg = comm.next_msg()
                self.msg_queue.put(new_msg)
        except Exception as e:
            logging.exception("exception in msg thread function")

if __name__ == '__main__':
    try:
        config = parse_args(**vars(args))
    except Exception as e:
        print(e)
        sys.exit(1)

    client = Client()

    try:
        msg_thread = threading.Thread(target=client.msg_thread_func)
        msg_thread.start()

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
