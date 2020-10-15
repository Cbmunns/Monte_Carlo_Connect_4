import numpy as np
import sys
import math
import random


ROWS = 6
COL = 7
tree = {}
key = 0


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
    def __init__(self, key, parent, move, board):
        self.key = key
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

def traverse(node):
    global tree
    global key

    best = 0
    best_weight = 0
    curr_weight = 0

    #look through children
    
    for i in range(len(node.children)):
        #print(tree[node.children[i]].visits)

        #if there is an unvisited node just select it
        if tree[node.children[i]].visits == 0:
            #print(0)
            return tree[node.children[i]].key
    for i in range(len(node.children)):
        # else get the weight of all children and choose the best
        curr_weight = (tree[node.children[i]].score/tree[node.children[i]].visits) + 2*(math.sqrt((math.log(tree[0].visits)/tree[node.children[i]].visits)))
        curr_weight = round(curr_weight,5)
        if curr_weight > best_weight:
            best_weight = curr_weight
            #print(tree[node.children[i]].key)
            best = tree[node.children[i]].key
            print(best)
            print("this: " + str(curr_weight) + str(best))
        

    # If the best value has children traverse them
    if tree[best].children != []:
        print(300)    
        traverse(tree[best])
    
    # Else we need to expand and create the best options children
    else:
        print(400)
        for i in range(0,7):
            #print(1999)
            #print_board(tree[best].board)
            #if that column has an empty spot, move is vaild
            if is_valid_location(tree[best].board, i):
                print(1999)
                #print(i)
                #find the lowest row you can place
                row = get_next_open_row(tree[best].board, i)
                #create node for move
                node = Node(key, tree[best].key, i, tree[best].board) 
                #place node in tree with key           
                tree[key] = node
                #add key of node as children of root
                tree[best].children.append(key)
                #print_board(tree[key].board)
                #place piece on that moves board
                drop_piece(tree[key].board, row, i, 2)
                print_board(tree[key].board)
                #increase key
                key += 1

        traverse(tree[best])

    
def rollout(node):

    board = np.copy(node.board)
    #print_board(board)
    game_over = False
    turn = 0
    spots_taken = 0
    score = 0
    
    
    #print(moves)
    while not game_over:
    
        
        #Ask for Player 1 Input:
        if turn == 0:
            selection = random.randrange(0,7)
            
            

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, 1)

                spots_taken += 1
                turn += 1
                turn = turn % 2

                if wining_move(board, 1):
                    
                    score = 1
                    game_over = True
                    #print_board(board)
            

        else:
            selection = random.randrange(0,7)
            
            
            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, 2)

                spots_taken += 1
                turn += 1
                turn = turn % 2

                if wining_move(board, 2):
                    
                    score = 2
                    game_over = True
                    #print_board(board)
            

        #print_board(board)
        #print()
        #print(spots_taken)

        if spots_taken == 42:
            score = 3
            #print_board(board)
            game_over = True
    return score


    


    
def backpropagate(node):
    global tree
    if node.parent != None:
        tree[node.parent].visits += node.visits
        tree[node.parent].score += node.score
        backpropagate(tree[node.parent])

def best_child(node):
    pass

def monte_carlo(board, player):
    #creat keys for nodes
    global key
    #create dict to hold tree
    global tree

    best_move = None
    best_weight = 0
    curr_weight = 0
    #make a copy of the board so we don't mess anything up
    copy_board = np.copy(board)
    #create empty root node that will hold total score, total moves, best move
    root = Node(key, None, None, copy_board)
    #place root in tree with key 0
    tree[key] = root
    #increase key
    key += 1

    #create initial moves in tree by parsing through any valid input
    for i in range(0,7):
        #if that column has an empty spot, move is vaild
        if is_valid_location(copy_board, i):
            #print(i)
            #find the lowest row you can place
            row = get_next_open_row(copy_board, i)
            #create node for move
            node = Node(key, tree[0].key, i, copy_board) 
            #place node in tree with key           
            tree[key] = node
            #add key of node as children of root
            tree[0].children.append(key)
            #print_board(tree[key].board)
            #place piece on that moves board
            drop_piece(tree[key].board, row, i, 2)
            #increase key
            key += 1

    #print_board(copy_board)
    # for i in range(len(tree[0].children)):
    #     print_board(tree[tree[0].children[i]].board)





    for i in range(8):
        print("hi")
        leaf_key = traverse(tree[0])
        simulation = rollout(tree[leaf_key])
        if simulation == player:
            point = 1
        elif simulation == 3:
            point = 0.5
        else:
            point = 0
        #print(point)
        tree[leaf_key].visits += 1
        tree[leaf_key].score += point
        backpropagate(tree[leaf_key])
        for i in range(7):
            x = tree[tree[0].children[i]].visits
            print(x)
        print(tree[0].visits)
        
        #print(tree[0].visits)
        #print(x.board)
        #print(leaf_key)
    
    final_move = None
    final_score = 0
    for i in range(7):
        x = tree[tree[0].children[i]].score

        if x > final_score:
            final_score = x
            final_move = tree[tree[0].children[i]].move


    return final_move



board = create_board()
#print_board(board)
x = monte_carlo(board, 2)
print(x)
#for i in range (1,8):
    #print_board(x[0].children[i].board)
