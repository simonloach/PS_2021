import logging
from enum import Enum

class PlayerState(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    IN_TURN = 2
    WAITING = 3

class MessageType(Enum):
    CONNECTED = 0
    NEW_GAME = 1
    YOUR_TURN = 2
    NEXT_MOVE = ord('1')
    MOVE_VALIDITY = 4
    BOARD_UPDATE = 5

class Player:
    def __init__(self, socket):
        self.socket = socket
        self.state = PlayerState.DISCONNECTED

    def init_game(self, game):
        self.game = game
        self.state = PlayerState.CONNECTED

    def update_state(self, new_state: PlayerState):
        self.state = new_state

    def send_msg(self, msg_type: MessageType, msg: bytes = b""):
        out = msg_type.value.to_bytes(1, "big") + msg
        logging.info(f"Sending: | {msg_type.value} | {msg} |\n {out}")
        self.socket.send(out)

    def wait_for_move(self):
        message = self.socket.recv(3)

        logging.info(f"Recieved: {message}")
        if len(message) != 3:
            logging.warning("got less bytes than anticipated")
            raise RuntimeError

        if message[0] != MessageType.NEXT_MOVE.value:
            logging.warning("Recieved wrong message type from client")
            raise RuntimeError

        x = message[1] - ord('1')
        y = message[2] - ord('1')
        return (x, y)
