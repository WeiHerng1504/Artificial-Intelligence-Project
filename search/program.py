# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import math
from .utils import render_board


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    ## calculation 
    # for every blue hex, check every red hex for distance
    # if closer distance found, record

    changableGrid = input
    blueHexes = check_grid(input, 'b')
    redHexes = check_grid(input, 'r')
    #print(blueHexes)
    #print(redHexes)
    list_of_moves = []

    shortest_distance = 100

    # (r, q) : (r direction, q direction)
    # optimal_move = ()

    # loop while there are still blue hexes on grid
    while check_grid(input, 'b'):

        for blueHex in blueHexes:
           for redHex in redHexes:
               
               move_considered = heuristic(blueHex, redHex)
               if move_considered[0] < shortest_distance:
                   shortest_distance = move_considered[0]
                   optimal_move = (redHex, move_considered[1])

        
        # normalise optimal move, NEEDS IMPROVEMENT

        if optimal_move[1][0] !=0:
            optimal_move[1][0] = int(optimal_move[1][0] / abs(optimal_move[1][0]))

        if optimal_move[1][1] !=0:
            optimal_move[1][1] = int(optimal_move[1][1] / abs(optimal_move[1][1]))

        
        #print(optimal_move)

        list_of_moves.append((optimal_move[0][0], optimal_move[0][1], optimal_move[1]))

        changableGrid = changeGrid(changableGrid, optimal_move, blueHexes, redHexes)[0]
        print(blueHex)
        
               
        
            

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]


def changeGrid(grid: dict[tuple, tuple], optimal_move: tuple, blueHexes: list, redHexes: list):

    # change starting hex power to 1
    # grid.update({(optimal_move[0][0], optimal_move[0][1]): ('r', 1)})
    
    # cahnge 


    # spread hexes
    for power in range(optimal_move[0][3]):
        r_new = optimal_move[0][0] + optimal_move[1][0] * power
        q_new = optimal_move[0][1] + optimal_move[1][1] * power

        # maybe change output of check_grid to dict? Then can use pop() instead of list comprehension
        blueHexes = [hex for hex in blueHexes if hex[0] != r_new and hex[1] != q_new]

        # update red hexes
        

        #grid.update({(r_new, q_new): ('r', (optimal_move[0][3] + 1) % 7)})
        

    return (grid, blueHexes)




# calculates and returns straight line distance
def heuristic(blueHex: tuple, redHex: tuple):

    # directions to move, normalized
    direction = [blueHex[0] - redHex[0], blueHex[1] - redHex[1]]

    # initial idea, NEEDS IMPROVEMENT!!!!
    if direction[0] > 3:
        direction[0] = direction[0] - 6
    elif direction[0] < -3:
        direction[0] = 6 + direction[0]

    if direction[1] > 3:
        direction[1] = direction[1] - 6
    elif direction[1] < -3:
        direction[1] = 6 + direction[1]
 
    
    #print('direction is ' + str(direction[0]) + ' ' + str(direction[1]))

    # make a spread action in the direction according to power
    afterSpread = (redHex[0] + direction[0]*redHex[3], redHex[1] + direction[1]*redHex[3])

    # calculate distance after spread to blueHex being considered
    distance = math.dist((blueHex[0], blueHex[1]), afterSpread)
    
    return (distance, direction)


# checks the current game state, returns dict of opponent tiles. If none, returns empty dict.
# takes dictionary of (r,q):(player,k) and colour 
def check_grid(input: dict[tuple, tuple], colour):
    tmp = dict()
    for key, value in input.items():
        if colour in value:
            tmp[key] =  value
    return tmp