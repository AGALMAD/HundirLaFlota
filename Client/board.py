class Board:
    def __init__(self):
        self.board = [["" for _ in range(10)] for _ in range(10)]


    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" %s |" % self.board[i][j], end="")
            print()

    def shot(self, x,y, good_shot):
        if self.board[x][y] == "" and good_shot:
            self.board[x][y] = "B"
        else:
            self.board[x][y] = "A"