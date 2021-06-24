import socket
import logging
from utils.definitions import MessageType

class ConnectionConfig:
    def __init__(self, ip_type, ip_addr, port):
        self.ip_type = ip_type
        self.ip_addr = ip_addr
        self.port = port

class Communicator:
    def __init__(self, config: ConnectionConfig ):
        self.config = config
        self.msg_buffer = bytes()
        self.socket = socket.socket(config.ip_type, socket.SOCK_STREAM)

    def connect(self):
        logging.info(f"Connecting to { self.config.ip_addr } on port {self.config.port}")
        self.socket.connect((self.config.ip_addr, int(self.config.port)))
        logging.info(f"Connected!")

    def send_move(self, x, y):
        self.socket.send(MessageType.NEXT_MOVE.value.to_bytes(1, "big") + x.encode() + y.encode() )

    def next_msg(self):
        if len(self.msg_buffer) < 2:
            self.msg_buffer += self.socket.recv(20);

        message_type = self.msg_buffer[0]

        if message_type == MessageType.CONNECTED.value:
            self.msg_buffer = self.msg_buffer[1:]
            return (MessageType.CONNECTED,)

        elif message_type == MessageType.NEW_GAME.value:
            cursor = self.msg_buffer[1]
            self.msg_buffer = self.msg_buffer[2:]
            return (MessageType.NEW_GAME, cursor)

        elif message_type == MessageType.YOUR_TURN.value:
            self.msg_buffer = self.msg_buffer[1:]
            return (MessageType.YOUR_TURN,)

        elif message_type == MessageType.MOVE_VALIDITY.value:
            validity = self.msg_buffer[1]
            self.msg_buffer = self.msg_buffer[2:]
            return (MessageType.NEW_GAME, validity)

        elif message_type == MessageType.BOARD_UPDATE.value:
            if len(self.msg_buffer) < 11:
                self.msg.msg_buffer += self.socket.recv(20)

            board = self.msg_buffer[1:10]
            self.msg_buffer = self.msg_buffer[10:]
            return (MessageType.BOARD_UPDATE, board)
