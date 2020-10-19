import numpy as np
import math
import random




# Constants for board size
ROWS = 6
COL = 7
# Create list of valid moves
moves = [0,1,2,3,4,5,6]

# Create board
def create_board():
    board = np.zeros((ROWS ,COL))
    return board
# Places piece on board
def drop_piece(board, row, selection, piece):
    board[row][selection] = piece
# Checks if column is full
def is_valid_location(board, selection):
    return board[ROWS-1][selection] == 0
# Finds the lowest open spot
def get_next_open_row(board, selection):
    for r in range(ROWS):
        if board[r][selection] == 0:
            return r

# Finds if the recent move is a winning one
def wining_move(board, piece):
    # Horizontal
    for c in range(COL-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                
                return True
    # Vertical
    for c in range(COL):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                
                return True
    # Ascending
    for c in range(COL-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                
                return True
    # Decending
    for c in range(COL-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                
                return True

# Create node class that is the basis of the Monte Carlo tree
class Node():
    def __init__(self, parent, move, board):
        # Holds its move, its working board, visits, accum score, children, and parent
        self.move = move
        self.board = np.copy(board)
        self.visits = 0
        self.score = 0.0
        self.children = []
        self.parent = parent

# Function for traversal and expansion
def traverse(node,player,opponent, exploration):
    
    # Set markers for tracking
    best = None
    best_weight = 0
    curr_weight = 0
    moves = [0,1,2,3,4,5,6]



    #look through children  
    for j in range(len(node.children)):
        
        #if there is an unvisited node just select it
        if node.children[j].visits == 0:
            
            return node.children[j]

    # Else get the weight of all children and choose the best
    for i in range(len(node.children)):
        
        curr_weight = (node.children[i].score/node.children[i].visits) + exploration*(math.sqrt((math.log(node.visits)/node.children[i].visits)))
        # Checks and holds the highest score
        if curr_weight > best_weight:
            best_weight = curr_weight
            # Record the position of best child in parent array
            best = i

    # if we are unable to calc weight return original node 
    if best == None:
        return node        
    
    
    # If the best weight has children traverse them
    if node.children[best].children != []:
           
        return traverse(node.children[best], player, opponent, exploration)
    
    # Else we need to expand and create the best options children
    else:
        # Generate some random move list for the opponent
        random.shuffle(moves)
        
        # Run through list and if a valid place is available, place and break
        for i in range (7):
            if is_valid_location(node.children[best].board, moves[0]):
                ro = get_next_open_row(node.children[best].board, moves[0])
                drop_piece(node.children[best].board, ro, moves[0], opponent)
                break
            # Pop the move that didn't work
            else:
                moves.pop(0)
        # If no move was valid, board was full return, original node
        if moves == []:
            return node
            

        # Generate all possible moves and place them in their own node
        for i in range(0,7):
            
            # If that column has an empty spot, move is vaild
            if is_valid_location(node.children[best].board, i):
                
                # Find the lowest row you can place
                row = get_next_open_row(node.children[best].board, i)
                # Create node for move
                no = Node(node.children[best], i, node.children[best].board) 
                # Place a move on that nodes board           
                drop_piece(no.board, row, i, player)
                # Add node as child of best parent
                node.children[best].children.append(no)
          
                
        # Then traverse those children
        return traverse(node.children[best], player, opponent, exploration)

# rollout by playing a dummy game with all random moves    
def rollout(node, player, opponent):
    # Use a temp board for this
    board = np.copy(node.board)
    # Create trackers
    game_over = False
    turn = 0
    score = 0 
    
    # While game is still going 
    while not game_over:
    
        
        # Player 1 Input:
        if turn == 0:
            # Random move
            random.shuffle(moves)            
            selection = moves[0]
            
            
            # Check if valid and place
            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, opponent)

                # Progress turn
                turn += 1
                turn = turn % 2

                # Break loop if winning move record score
                if wining_move(board, opponent):
                    score = opponent
                    game_over = True
                    
            
        # Player 1 Input:
        else:
            # Random move
            random.shuffle(moves)            
            selection = moves[0]
            
            # Check if valid and place
            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, player)

                # Progress turn
                turn += 1
                turn = turn % 2

                # Break loop if winning move record score
                if wining_move(board, player):
                    
                    score = player
                    game_over = True
                    
        # Since the board could be in any state just check if there are open spots   
        count = 0
        for c in range(COL):
            for r in range(ROWS):
                if board[r][c] == 0:
                    count += 1

        # If no open spots break and record score for draw
        if count == 0:
            score = 3
            
            game_over = True
    # Return score of game
    return score


    


# Backprop the parents until you reach root  
def backpropagate(node, score):
    
    node.parent.visits += 1
    node.parent.score += score
    if node.parent.move != None:
        backpropagate(node.parent, score)

# Main driver function
def monte_carlo(copy, player, opponent, exploration, iteration):
       
    # Create empty root node that will hold total score, total moves
    root = Node(None, None, copy)    

    # Create initial moves in tree by parsing through any valid input
    for i in range(0,7):
        # If that column has an empty spot, move is vaild
        if is_valid_location(root.board, i):
            
            # Find the lowest row you can place
            row = get_next_open_row(root.board, i)
            # Create node for move
            node = Node(root, i, root.board) 
            # Place a move on that nodes board           
            drop_piece(node.board, row, i, player)
            # Add node as child of best parent
            root.children.append(node)

    # For for how ever many times we want to run the simulation        
    for i in range(iteration):
        # Traverse tree and expand as needed to find best candidate
        leaf_node = traverse(root, player, opponent, exploration)
        # rollout the simulation and get the score
        simulation = rollout(leaf_node, player, opponent)
        if simulation == player:
            point = 1
        elif simulation == 3:
            point = 0.5
        else:
            point = 0
        # Add a visit to this node and the score that was earned win/lose/draw
        leaf_node.visits += 1
        leaf_node.score += point
        # Backprop up to the root
        backpropagate(leaf_node, point)
        
    # Trackers for the winning move
    final_move = None
    final_score = 0
    # Search children of root for best move based on score
    for i in range(len(root.children)):
        x = root.children[i].score
        if x > final_score:
            final_score = x
            final_move = root.children[i].move

    # Return the best score
    return final_move
