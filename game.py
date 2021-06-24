from player import MessageType, Player, PlayerState


class Game:
    def __init__(self, player1: Player, player2: Player):
        player1.init_game(self)
        player2.init_game(self)
        self.players = [player1, player2]
        self.current_player = 0
        self.board = [0]*9 # 0 - empty, 1 - circle, 2 - cross

    def start(self):
        self.players[self.current_player].send_msg(MessageType.YOUR_TURN)
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
        if self.check_for_win(): 
            self.players[self.current_player].update_state(PlayerState.FINISHED)
            self.players[next_player].update_state(PlayerState.FINISHED)
            return True
        self.players[next_player].send_msg(MessageType.YOUR_TURN)
        self.current_player = next_player
        return True
    
    def check_for_win(self):
        WINNING_CASES = [
            [[i, i+1, i+2] for i in range(0,9,3)], # HORIZONTALs
            [[i, i+3, i+6] for i in range(0,3,1)], # VERTICALs
            [[1+i, 4, 7-i] for i in range(-1,2,2)] # DIAGONALs
            ]

        for TYPE_OF_CASE in WINNING_CASES:
            for CASE in TYPE_OF_CASE:
                if self.board[CASE[0]] == 0 or self.board[CASE[1]] == 0 or self.board[CASE[2]] == 0:
                    continue
                if self.board[CASE[0]] == self.board[CASE[1]] == self.board[CASE[2]]:
                    return True

        return False