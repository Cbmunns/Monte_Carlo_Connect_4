import numpy as np

rows = 6
col = 7



def create_board():
    board = np.zeros((rows ,col))
    return board

def drop_piece(board, row, selection, piece):
    board[row][selection] = piece

def is_valid_location(board, selection):
    return board[rows-1][selection] == 0

def get_next_open_row(board, selection):
    for r in range(rows):
        if board[r][selection] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def wining_move(board, piece):
    #hori
    for c in range(col-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] and board[r][c+3] == piece:
                return True
    #vertical
    for c in range(col):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] and board[r+3][c] == piece:
                return True
    #ascending
    for c in range(col-3):
    	for r in range(rows-3):
		    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
			    return True
    #decending
    for c in range(col-3):
    	for r in range(3, rows):
		    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
			    return True

board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    #Ask for Player 1 Input:
    if turn == 0:
        selection = int(input("Player 1 make your selection 1-7: "))
        selection -= 1

        if is_valid_location(board, selection):
            row = get_next_open_row(board, selection)
            drop_piece(board, row, selection, 1)

            if wining_move(board, 1):
                print("Player 1 wins!")
                game_over = True

    else:
        selection = int(input("Player 2 make your selection 1-7: "))
        selection -= 1

        if is_valid_location(board, selection):
            row = get_next_open_row(board, selection)
            drop_piece(board, row, selection, 2)

            if wining_move(board, 2):
                print("Player 2 wins!")
                game_over = True

    print_board(board)
    turn += 1
    turn = turn % 2