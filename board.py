class Board:
    def __init__(self):
        self.board = [0]*9
        self.messages = list()
        
    def __repr__(self):
        self.printable = list()
        for el in self.board:
            if el == 0:
                self.printable.append(" ")
            elif el == 1:
                self.printable.append(u"\u2B58")
            elif el== 2:
                self.printable.append(u"\u2716")

        template = '''
\t       _________________
\t      |     |     |     |
\t     X|  1  |  2  |  3  |
\t __Y__|_____|_____|_____|
\t|     |     |     |     |
\t|  1  |  {}  |  {}  |  {}  |
\t|_____|_____|_____|_____|
\t|     |     |     |     |
\t|  2  |  {}  |  {}  |  {}  |              
\t|_____|_____|_____|_____|
\t|     |     |     |     |
\t|  3  |  {}  |  {}  |  {}  |
\t|_____|_____|_____|_____|
'''
        result = template.format(*self.printable).splitlines()
        output = chr(27) + "[2J"
        output += result.pop(0) + '\n'
        output += result.pop(0) + '\n'
        while len(result)>0 or len(self.messages)>0:
            if len(result)==0:
                output += "\t                         \t" + self.messages.pop(0) + '\n'
            elif len(self.messages) == 0:
                output += result.pop(0) + '\n'
            else:
                output += result.pop(0) + '\t' + self.messages.pop(0) + '\n'
        return output
    
    def update_board(self, new_board: bytes):
        self.board = list(new_board)

    def update_board_with_local(self, last_move, cursor):
        index = int(last_move[0]) - 1 + (int(last_move[1]) - 1) * 3
        self.board[index] = cursor

    def add_message(self, message):
        self.messages.append(message)
    
    def remove_message(self, message):
        self.messages.pop(self.messages.index(message))

    def clear_board(self):
        self.board = [0]*9

b = Board()
print(b)