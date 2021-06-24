from enum import Enum

class MessageType(Enum):
    CONNECTED = 0
    NEW_GAME = 1
    YOUR_TURN = 2
    NEXT_MOVE = 3
    MOVE_VALIDITY = 4
    BOARD_UPDATE = 5