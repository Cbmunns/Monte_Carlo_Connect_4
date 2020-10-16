import random
arr = []

curr_weight = (0/0) + 7*(math.sqrt((math.log(0)/0)))

class Board():
    def __init__(self, rows, col):
        self.board = np.zeros((rows, col))
        self.rows = rows
        self.col = col
        
    #places piece on board
    def drop_piece(self, row, selection, piece):
        self.board[row][selection] = piece

    #checks if column is full    
    def is_valid_location(self, selection):
        return self.board[self.rows-1][selection] == 0

    #finds the lowest open spot
    def get_next_open_row(self, selection):
        for r in range(self.rows):
            if self.board[r][selection] == 0:
                return r

    #reverse board to be more easily read
    def print_board(self):
        print(np.flip(self.board, 0))
    
    def wining_move(self, piece):
        #horizontal
        for c in range(self.col-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    print("Horizontal Win Player: " + str(piece))
                    print()
                    return True
        #vertical
        for c in range(self.col):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    print("Vertical Win Player:  " + str(piece))
                    print()
                    return True
        #ascending
        for c in range(self.col-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    print("Ascending Win Player "+ str(piece))
                    print()
                    return True
        #decending
        for c in range(self.col-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    print("Descending Win Player: " + str(piece))
                    print()
                    return True