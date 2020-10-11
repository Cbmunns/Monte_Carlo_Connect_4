import numpy as np

rows = 6
col = 7



def create_board():
    board = np.zeros((rows ,col))
    return board

def drop_piece(board, row, selection, piece):
    board[row][selection] = piece

def is_valid_location(board, selection):
    return board[5][selection] == 0

def get_next_open_row(board, selection):
    for r in range(rows):
        if board[r][selection] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

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

    else:
        selection = int(input("Player 2 make your selection 1-7: "))
        selection -= 1

        if is_valid_location(board, selection):
            row = get_next_open_row(board, selection)
            drop_piece(board, row, selection, 2)

    print_board(board)
    turn += 1
    turn = turn % 2