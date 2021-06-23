from player import Player, PlayerState

class Game:
    def __init__(self, player1: Player, player2: Player):
        player1.start_game(self)
        player2.start_game(self)
        self.players = [player1, player2]
        self.current_player = 0
        self.board = [[0, 0, 0]]*3 # 0 - empty, 1 - circle, 2 - cross

    def is_now_my_turn(self, player: Player):
        return self.players[self.current_player].socket == player.socket

    def move(self, move):
        # alter self.board
        # send board to other player
        # change self.current_player
        pass
