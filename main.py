import pygame
import pygame.freetype
import pygame_menu


count = None
arr = []

game_type = None

player = None


def show_board(board):
    global count
    print() 
    print("    Moves made: ", count)
    for i in range(0, 7):
        print(board[i])
    count += 1
    print()

def swap_player(current):    
    if current == "Player_1":
        return "Player_2"
    else:
        return "Player_1"


def create_board():
    """
    This creates the board with usable and unusable coordinates
    """
    # Set the rows and the columns to 7
    col = 8 
    row = 7
    global arr
    arr = []
    rows = 6
    columns = 1
    # Create a 2D Array full of 0's with 6 rows and 7 columns
    arr = [[0 for i in range(col)] for j in range(row)]

    for i in range (6):
        arr[i][0] = rows
        rows -= 1 
    for i in range (7):
        arr[6][i+1] = columns
        columns += 1 

    
    return arr


def place_piece(player):
    global arr
    global count
    coord = [0]*2

    placed = False

    show_board(arr)

    print("Okay ", player, " pick a position")
    x = input("x: ")
 
    while x not in ["1","2","3","4","5","6","7"]:
        print()   
        print("---------------------------")
        print(" Incorrect input, try 1-7")
        print("---------------------------")
        print()
        count -= 1
        show_board(arr)
        x = input("x: ")
    
    while placed == False:
        if arr[0][int(x)] != 0:
            print()   
            print("---------------------------")
            print("Column full, choose another")
            print("---------------------------")
            print()
            count -= 1
            show_board(arr)
            x = input("x: ")
            while x not in ["1","2","3","4","5","6","7"]:
                print()   
                print("---------------------------")
                print(" Incorrect input, try 1-7")
                print("---------------------------")
                print()
                count -= 1
                show_board(arr)
                x = input("x: ")
        else:
            placed = True


    if player == "Player_1":
            for  i in reversed(range(7)):
                if arr[i][int(x)] == 0:
                    #arr[i][int(x)] = 1
                    coord[0] = i
                    coord[1] = int(x)
                    return coord
            


            
    elif player == "Player_2":
        for  i in reversed(range(7)):
            if arr[i][int(x)] == 0:
                coord[0] = i
                coord[1] = int(x)
                return coord

def check_win(place, player):
    global arr
    win = False
    count = 0

    if player == "Player_1":
        piece = 1
    else:
        piece = 2

    #ascending

    #descending
    count = 0
    for i in range(6):
        if place[0]+i < 6 and place[1]+i < 8:
            if arr[place[0]+i][place[1]+i] == piece:
                count += 1
    for i in range(1,6):
        if place[0]-i > -1 and place[1]-i > 0:
            if arr[place[0]-i][place[1]-i] == piece :
                count += 1
    if count == 4:
        show_board(arr)
        win = True

    #horizontal
    count = 0
    for i in range(1,8):
        if arr[place[0]][i] == piece:
            count += 1
    if count == 4:
        show_board(arr)
        win = True


    #vertical
    count = 0
    for i in range(6):
        if arr[i][place[1]] == piece:
            count += 1      
    if count == 4:
        show_board(arr)
        win = True

    return win


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
        human_computer()
        



    elif game_type == "2":
        print("computer")
        show_board(arr)

def human_computer():
    global player
    global arr
    global count

    win = False
    
    player = "Player_1"
    count = 0

    create_board()

    while win == False:
        place = place_piece(player)
        print (place[1], 6 - place[0])
        if player == "Player_1":
            arr[place[0]][place[1]] = 1
        if player == "Player_2":
            arr[place[0]][place[1]] = 2

        win = check_win(place, player)
        player = swap_player(player)



        if count == 42:
            win = True
    print("It was a draw!")
    menu()


#driver code
menu()
    

