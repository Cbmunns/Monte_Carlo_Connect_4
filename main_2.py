import numpy as np
import sys
import math


ROWS = 6
COL = 7


#create board
def create_board():
    board = np.zeros((ROWS ,COL))
    return board
#places piece on board
def drop_piece(board, row, selection, piece):
    board[row][selection] = piece
#checks if column is full
def is_valid_location(board, selection):
    return board[ROWS-1][selection] == 0
#finds the lowest open spot
def get_next_open_row(board, selection):
    for r in range(ROWS):
        if board[r][selection] == 0:
            return r
#reverse board to be more easily read
def print_board(board):
    print(np.flip(board, 0))


def wining_move(board, piece):
    #horizontal
    for c in range(COL-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                print("hor " + str(piece))
                print()
                return True
    #vertical
    for c in range(COL):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                print("vert " + str(piece))
                print()
                return True
    #ascending
    for c in range(COL-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                print("asc "+ str(piece))
                print()
                return True
    #decending
    for c in range(COL-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                print("desc " + str(piece))
                print()
                return True

def proper_piece():   

    x = input("Player 1 make your selection 1-7 or Q to quit: ")
 
    while x not in ["1","2","3","4","5","6","7","Q"]:
        
        print()   
        print("---------------------------")
        print(" Incorrect input, try 1-7")
        print("---------------------------")
        print()
        x = input("x: ")

    if x == "Q":
            sys.exit()
    return x



def play_game():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0
    spots_taken = 0
    score = 0
    
    while not game_over:

        
        #Ask for Player 1 Input:
        if turn == 0:
            selection = int(proper_piece())
            print()
            selection -= 1

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, 1)

                spots_taken += 1
                turn += 1
                turn = turn % 2

                if wining_move(board, 1):
                    
                    score = 1
                    game_over = True
            else:
                print()   
                print("---------------------------")
                print("Column full, choose another")
                print("---------------------------")
                print()

        else:
            selection = int(proper_piece())
            print()
            selection -= 1

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, 2)

                spots_taken += 1
                turn += 1
                turn = turn % 2

                if wining_move(board, 2):
                    
                    score = 2
                    game_over = True
            else:
                print()   
                print("---------------------------")
                print("Column full, choose another")
                print("---------------------------")
                print()

        print_board(board)
        print()
        #print(spots_taken)

        if spots_taken == 42:
            game_over = True


    if score == 1:
        print("Player 1 wins!")
    elif score == 2:
        print("Player 2 wins!")
    else: 
        print("It's a draw!")

def menu():
    
    print()
    print("       Hello and welcome to Connect 4!")
    print("Please make a selection from the choices below!")
    print("           1. Human Vs Computer")
    print("           2. Computer vs Computer")
    game_type = input("           What is your selection? ")

    while game_type != "1" and game_type != "2":
        print()
        print("       incorrect selection! try again!")
        print()
        print("       Hello and welcome to Connect 4!")
        print("Please make a selection from the choices below!")
        print("           1. Human Vs Computer")
        print("           2. Computer vs Computer")
        game_type = input("           What is your selection? ")

    if game_type == "1":
        print()
        print("Human Vs Computer")
        print()
        play_game()
        



    elif game_type == "2":
        print()
        print("Computer vs Computer")
        print()
        play_game()


menu()