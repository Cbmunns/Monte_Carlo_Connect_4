import numpy as np
import sys
import math
import random


ROWS = 6
COL = 7
root = None
total_visits = 0
moves = [0,1,2,3,4,5,6]

def create_board():
    board = np.zeros((ROWS ,COL))
    return board

def drop_piece(board, row, selection, piece):
    board[row][selection] = piece

def is_valid_location(board, selection):
    return board[ROWS-1][selection] == 0

def get_next_open_row(board, selection):
    for r in range(ROWS):
        if board[r][selection] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def wining_move(board, piece):
    #horizontal
    for c in range(COL-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                #print("hor " + str(piece))
                #print()
                return True
    #vertical
    for c in range(COL):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                #print("vert " + str(piece))
                #print()
                return True
    #ascending
    for c in range(COL-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                #print("asc "+ str(piece))
                #print()
                return True
    #decending
    for c in range(COL-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                #print("desc " + str(piece))
                #print()
                return True


class Node():
    def __init__(self, parent, move, board):
        
        self.move = move
        self.board = np.copy(board)
        self.visits = 0
        self.score = 0.0
        self.weight = 0
        self.children = []
        self.parent = parent

    def calc_weight(total_weight, visits, score):
        weight = (score/visits) + 2*(math.sqrt((math.log(total_weight)/visits)))

        return weight

    


def search_leaf_nodes(root, leafs):   

    #if node is empty return
    if root == None:
        return

    #if no children then leaf, return data
    if root.children == []:
        return root.state.append(leafs)

    #if it has children search through them
    for i in range(root.children):
        search_leaf_nodes(root.children[i])

def traverse(node,player,opponent):
    global root

    best = 0
    best_weight = 0
    curr_weight = 0

    #look through children
    
    
    for j in range(len(node.children)):
        
        #if there is an unvisited node just select it
        if node.children[j].visits == 0:
            
            return node.children[j]
    
    for i in range(len(node.children)):
        constant = 7
        # else get the weight of all children and choose the best
        curr_weight = (node.children[i].score/node.children[i].visits) + constant*(math.sqrt((math.log(node.visits)/node.children[i].visits)))
        
        if curr_weight > best_weight:
            best_weight = curr_weight
            
            best = i
            
    
    
    # If the best value has children traverse them
    if node.children[best].children != []:
           
        return traverse(node.children[best], player, opponent)
    
    # Else we need to expand and create the best options children
    else:
        
        random.shuffle(moves)
        j = moves[0]
        while is_valid_location(node.children[best].board, j) == False:
            random.shuffle(moves)
            j = moves[0]
        ro = get_next_open_row(node.children[best].board, j)
        drop_piece(node.children[best].board, ro, j, opponent)


        for i in range(0,7):
            
            #if that column has an empty spot, move is vaild
            if is_valid_location(node.children[best].board, i):
                
                #find the lowest row you can place
                row = get_next_open_row(node.children[best].board, i)
                #create node for move
                no = Node(node.children[best], i, node.children[best].board) 
                #place node in tree with key           
                drop_piece(no.board, row, i, player)
                #add key of node as children of root
                node.children[best].children.append(no)
          
                
        
        return traverse(node.children[best], player, opponent)

    
def rollout(node, player, opponent):

    board = np.copy(node.board)
    
    game_over = False
    turn = 0
    l = False
    score = 0
    
    
    
    while not game_over:
    
        
        #Ask for Player 1 Input:
        if turn == 0:
            random.shuffle(moves)            
            selection = moves[0]
            
            

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, opponent)

                
                turn += 1
                turn = turn % 2

                if wining_move(board, 1):
                    score = opponent
                    game_over = True
                    
            

        else:
            random.shuffle(moves)            
            selection = moves[0]
            
            
            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, player)

                
                turn += 1
                turn = turn % 2

                if wining_move(board, 2):
                    
                    score = player
                    game_over = True
                    
            
        count = 0
        for c in range(COL):
            for r in range(ROWS):
                if board[r][c] == 0:
                    count += 1

        if count == 0:
            score = 3
            
            game_over = True
    return score


    


    
def backpropagate(node, score):
    
    node.parent.visits += 1
    node.parent.score += score
    if node.parent.move != None:
        backpropagate(node.parent, score)

def best_child(node):
    pass

def monte_carlo(board, player, opponent):
    
    global root
    
    
    #create empty root node that will hold total score, total moves, best move
    root = Node(None, None, board)
    

    #create initial moves in tree by parsing through any valid input
    for i in range(0,7):
        #if that column has an empty spot, move is vaild
        if is_valid_location(root.board, i):
            print("ding")
            #find the lowest row you can place
            row = get_next_open_row(root.board, i)
            #create node for move
            node = Node(root, i, root.board) 
            #place node in tree with key           
            drop_piece(node.board, row, i, player)
            #add key of node as children of root
            root.children.append(node)
            
    for i in range(1000):
        
        leaf_node = traverse(root, player, opponent)
        
        simulation = rollout(leaf_node, player, opponent)
        if simulation == player:
            point = 1
        elif simulation == 3:
            point = 0.5
        else:
            point = 0
        
        leaf_node.visits += 1
        leaf_node.score += point
        
        backpropagate(leaf_node, point)
        
    
    final_move = None
    final_score = 0
    for i in range(len(root.children)):
        x = root.children[i].score
        if x > final_score:
            final_score = x
            final_move = root.children[i].move


    return final_move
