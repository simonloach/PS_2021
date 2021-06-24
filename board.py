class Board:
    def __init__(self):
        self.board = [0]*9
        
    def __repr__(self):
        self.printable = list()
        for el in self.board:
            if el == 0:
                self.printable.append(" ")
            elif el == 1:
                self.printable.append(u"\u2B58")
            elif el== 2:
                self.printable.append(u"\u2716")

        result = f'''
    \t       _________________
    \t      |     |     |     |
    \t     X|  1  |  2  |  3  |
    \t __Y__|_____|_____|_____|
    \t|     |     |     |     |
    \t|  1  |  {self.printable[0]}  |  {self.printable[1]}  |  {self.printable[2]}  |
    \t|_____|_____|_____|_____|
    \t|     |     |     |     |
    \t|  2  |  {self.printable[3]}  |  {self.printable[4]}  |  {self.printable[5]}  |
    \t|_____|_____|_____|_____|
    \t|     |     |     |     |
    \t|  3  |  {self.printable[6]}  |  {self.printable[7]}  |  {self.printable[8]}  |
    \t|_____|_____|_____|_____|
    '''
        return result  
    
    def update_board(self, new_board: bytes):
        self.board = list(new_board)
b = Board()
print(b)