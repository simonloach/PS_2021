import socket
import logging
from typing import Sequence
from utils.definitions import MessageType

class Message:
    def __init__(self, msg_type, payload = None):
        self.type = msg_type
        self.payload = payload

    def encode(self, value):
        if type(value) == str:
            return value.encode()
        elif type(value) == int:
            return value.to_bytes(1, "little")
        elif isinstance(value, Sequence):
            return b"".join([self.encode(x) for x in value])

    def encode_message(self):
        return self.type.value.to_bytes(1, "little") + self.encode(self.payload)

class Communicator:
    def __init__(self, config: dict):
        self.config = config
        self.msg_buffer = bytes()
        self.socket = socket.socket(config["ip_type"], socket.SOCK_STREAM)

    def connect(self):
        logging.info(f"Connecting to { self.config['ip_addr'] } on port {self.config['port']}")
        self.socket.connect((self.config['ip_addr'], int(self.config['port'])))
        logging.info(f"Connected!")

    def send_msg(self, msg: Message):
        self.socket.send(msg.encode_message())

    def next_msg(self):
        if len(self.msg_buffer) < 1:
            self.msg_buffer += self.socket.recv(20);

        message_type = self.msg_buffer[0]

        if message_type == MessageType.CONNECTED.value:
            self.msg_buffer = self.msg_buffer[1:]
            return Message(MessageType.CONNECTED)

        elif message_type == MessageType.NEW_GAME.value:
            cursor = self.msg_buffer[1]
            self.msg_buffer = self.msg_buffer[2:]
            return Message(MessageType.NEW_GAME, cursor)

        elif message_type == MessageType.YOUR_TURN.value:
            self.msg_buffer = self.msg_buffer[1:]
            return Message(MessageType.YOUR_TURN)

        elif message_type == MessageType.MOVE_VALIDITY.value:
            validity = self.msg_buffer[1]
            self.msg_buffer = self.msg_buffer[2:]
            return Message(MessageType.MOVE_VALIDITY, validity)

        elif message_type == MessageType.BOARD_UPDATE.value:
            if len(self.msg_buffer) < 11:
                self.msg_buffer += self.socket.recv(20)

            board = self.msg_buffer[1:10]
            self.msg_buffer = self.msg_buffer[10:]
            return Message(MessageType.BOARD_UPDATE, board)
