import numpy as np
import sys
from monte_carlo_tree_search import monte_carlo


# Constants for board size
ROWS = 6
COL = 7

# Create class for board
class Board():
    # Holds a numpy board and the size parameters
    def __init__(self, rows, col):
        self.board = np.zeros((rows, col))
        self.rows = rows
        self.col = col
        
    # Places piece on board
    def drop_piece(self, row, selection, piece):
        self.board[row][selection] = piece

    # Checks if column is full    
    def is_valid_location(self, selection):
        print(self.board[self.rows-1][selection])
        return self.board[self.rows-1][selection] == 0

    # Finds the lowest open spot
    def get_next_open_row(self, selection):
        for r in range(self.rows):
            if self.board[r][selection] == 0:
                return r

    # Reverse board to be more easily read
    def print_board(self):
        print(np.flip(self.board, 0))
        
    
    # Finds if the recent move is a winning one
    def wining_move(self, piece):
        # Horizontal
        for c in range(self.col-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    print("Horizontal Win Player: " + str(piece))
                    print()
                    return True
        # Vertical
        for c in range(self.col):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    print("Vertical Win Player:  " + str(piece))
                    print()
                    return True
        # Ascending
        for c in range(self.col-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    print("Ascending Win Player "+ str(piece))
                    print()
                    return True
        # Decending
        for c in range(self.col-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    print("Descending Win Player: " + str(piece))
                    print()
                    return True


# Check to see if the human input is valid to be played
def proper_piece():

    # Take in input
    x = input("Player 1 make your selection 1-7 or Q to quit: ")
    # Check if valid, if not repeat
    while x not in ["1","2","3","4","5","6","7","Q"]:
        
        print()   
        print("---------------------------")
        print(" Incorrect input, try 1-7")
        print("---------------------------")
        print()
        x = input("x: ")
    # If Q exit program all together
    if x == "Q":
            sys.exit()
    # Return the move
    return x

# Define how a human player selects a piece
def human_player():
    selection = int(proper_piece())
    print()
    selection -= 1
    return selection

# Define how a computer selects a piece AKA Monte Carlo
def computer_player(board, player, opponent, exploration, iteration):
    print("---------------------------")
    print("    Computer Thinking")
    print("---------------------------")
    selection = monte_carlo(board.board, player, opponent, exploration, iteration)
    return selection
    
# define how the game works
def play_game(exploration, iteration, human):
    # Create board and print it
    board = Board(ROWS,COL)
    board.print_board()

    # Establish tracked variables
    turn = 0
    spots_taken = 0
    score = 0
    comp_1 = False
    comp_2 = False
    game_over = False

    # Check if Human chose first or second move
    if human == 1 or human == 0:
        comp = 2
    else:
        comp = 1
    
    # Start game
    while not game_over:
        
        #Ask for Player 1 Input:
        if turn == 0:
            # Check if human or computer get piece
            if human == 1:
                selection = human_player()
            elif human == 0:
                selection = computer_player(board, comp, human + 1, exploration, iteration)
                comp_1 = True
            else:
                selection = computer_player(board, comp, human, exploration, iteration)
                comp_1 = True
            # Check if this was a valid move
            if board.is_valid_location(selection):
                # Grab the appropriate row
                row = board.get_next_open_row(selection)
                # Place it on the board
                board.drop_piece(row, selection, 1)

                # Add spot taken, progress turn, print board 
                spots_taken += 1
                turn += 1
                turn = turn % 2
                board.print_board()
                print()

                # If winning move break loop add score
                if board.wining_move(1):
                    
                    score = 1
                    game_over = True
            # Invalid move loop for another selection
            else:
                print()   
                print("---------------------------")
                print("Column full, choose another")
                print("---------------------------")
                print()
        # Ask for Player 2 Inpute
        else:
            # Check if human or computer get piece
            if human == 2:
                selection = human_player()
            else:
                selection = computer_player(board, comp, human + 1, exploration, iteration)
                comp_2 = True
            # Check if this was a valid move
            if board.is_valid_location(selection):
                # Grab the appropriate row
                row = board.get_next_open_row(selection)
                # Place it on the board
                board.drop_piece(row, selection, 2)

                # Add spot taken, progress turn, print board
                spots_taken += 1
                turn += 1
                turn = turn % 2
                board.print_board()
                print()

                # If winning move break loop add score
                if board.wining_move(2):
                    
                    score = 2
                    game_over = True
            # Invalid move loop for another selection
            else:
                print()   
                print("---------------------------")
                print("Column full, choose another")
                print("---------------------------")
                print()

        # If all spots are taken break loop
        if spots_taken == 42:
            game_over = True

    # If player 1 won
    if score == 1:
        if comp_1:
            print("Computer Player 1 wins!")
        else:
            print("Player 1 wins!")
    # If player 2 won
    elif score == 2:
        if comp_2:
            print("Computer Player 2 wins!")
        else:
            print("Player 2 wins!")
    # If draw
    else: 
        print("It's a draw!")


# Create opening menu function
def menu():
    
    # Display splash screen with choices between two game types
    print()
    print("       Hello and welcome to Connect 4!")
    print("Please make a selection from the choices below!")
    print("           1. Human vs Computer")
    print("           2. Computer vs Computer")
    game_type = input("           What is your selection? ")

    # Loop if invalid choice
    while game_type != "1" and game_type != "2":
        print()
        print("       incorrect selection! try again!")
        print()
        print("       Hello and welcome to Connect 4!")
        print("Please make a selection from the choices below!")
        print("           1. Human vs Computer")
        print("           2. Computer vs Computer")
        game_type = input("           What is your selection? ")

    # If 1 Human vs Computer collect exploration constant, Monte Carlo iterations and
    # whether they want to go first or second
    if game_type == "1":
        print()
        print("              Human Vs Computer")
        print()
        exploration = input("How much do you want to favor exploration?: ")
        print()
        iterations = input("How many iterations for Monte Carlo? [Any number]: ")
        print()
        human =       input("Do you want to go first or second? [1 or 2]: ")
        play_game(int(exploration),int(iterations), int(human))
        


    # If 2 Computer vs Computer collect exploration constant, Monte Carlo iterations
    elif game_type == "2":
        print()
        print("Computer vs Computer")
        print()
        exploration = input("How much do you want to favor exploration?: ")
        print()
        iterations = input("How many iterations for Monte Carlo? [Any number]: ")
        print()
        human = 0
        play_game(int(exploration),int(iterations), int(human))
        


menu()