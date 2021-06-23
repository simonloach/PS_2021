from player import MessageType, Player, PlayerState

class Game:
    def __init__(self, player1: Player, player2: Player):
        player1.init_game(self)
        player2.init_game(self)
        self.players = [player1, player2]
        self.current_player = 0
        self.board = [0]*9 # 0 - empty, 1 - circle, 2 - cross

    def start(self):
        self.players[self.current_player].update_state(PlayerState.IN_TURN)

    def is_now_my_turn(self, player: Player):
        return self.players[self.current_player].socket == player.socket

    def move(self, move):
        (x, y) = move
        idx = y * 3 + x
        if x > 3 and y > 3:
            return False
        if self.board[idx] != 0:
            return False
        self.board[idx] = self.current_player + 1

        next_player = (self.current_player + 1) % 2
        self.players[next_player].send_msg(MessageType.BOARD_UPDATE, bytes(self.board))
        self.players[self.current_player].update_state(PlayerState.WAITING)
        self.players[next_player].update_state(PlayerState.IN_TURN)
        self.current_player = next_player;
        return True
