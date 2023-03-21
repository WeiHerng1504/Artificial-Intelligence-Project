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

    blueHexes = check_grid(input, 'b')
    redHexes = check_grid(input, 'r')
    list_of_moves = []

    # loop while there are still blue hexes on grid
    while blueHexes:

        shortest_distance = 1000

        for blueHex in blueHexes.keys():
           for redHex in redHexes.keys():
               
               move_considered = heuristic(blueHex + blueHexes[blueHex], redHex + redHexes[redHex])
               if (move_considered[0] < shortest_distance) and (move_considered[1][0]*move_considered[1][1] <= 0):
                    #print('inside if statement ' + str(move_considered))
                    shortest_distance = move_considered[0]
                    #print("blueHex is " + str(blueHex) + ", redHXe is " + str(redHex))
                    optimal_move = (redHex + redHexes[redHex], move_considered[1])

      
        # normalise optimal move, NEEDS IMPROVEMENT
        if optimal_move[1][0] !=0:
            optimal_move[1][0] = int(optimal_move[1][0] / abs(optimal_move[1][0]))

        if optimal_move[1][1] !=0:
            optimal_move[1][1] = int(optimal_move[1][1] / abs(optimal_move[1][1]))


        list_of_moves.append((optimal_move[0][0], optimal_move[0][1], optimal_move[1][0], optimal_move[1][1]))
        
        changeGrid(optimal_move, blueHexes, redHexes)
            

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...


    return list_of_moves

    


def changeGrid(optimal_move: tuple, blueHexes: dict, redHexes: dict):

    # change starting hex power to 0
    #redHexes.update({(optimal_move[0][0], optimal_move[0][1]): ('r', 1)})
    redHexes.pop((optimal_move[0][0], optimal_move[0][1]), None)
    
    # cahnge 


    # spread hexes, need to handle maximum power
    for power in range(1, optimal_move[0][3] + 1):

        r_new = (optimal_move[0][0] + optimal_move[1][0] * power) % 7
        q_new = (optimal_move[0][1] + optimal_move[1][1] * power) % 7

        # convert blue to red
        if (r_new, q_new) in blueHexes:
            redHexes.update({(r_new, q_new): (blueHexes[(r_new, q_new)])})
            blueHexes.pop((r_new, q_new), None)

        # update red hexes
        if (r_new, q_new) in redHexes:
            redHexes.update({(r_new, q_new): ('r', redHexes[(r_new, q_new)][1] + 1)})
            if redHexes[(r_new, q_new)][1] == 6:
                redHexes.pop((r_new, q_new), None)
        else:
            redHexes.update({(r_new, q_new): ('r', 1)})

    return (blueHexes, redHexes)




# calculates and returns straight line distance
def heuristic(blueHex: tuple, redHex: tuple):

    # directions to move, normalized
    direction = [blueHex[0] - redHex[0], blueHex[1] - redHex[1]]

    # initial idea, NEEDS IMPROVEMENT!!!!
    if direction[0] > 3:
        direction[0] = direction[0] - 7
    elif direction[0] < -3:
        direction[0] = 7 + direction[0]

    if direction[1] > 3:
        direction[1] = direction[1] - 7
    elif direction[1] < -3:
        direction[1] = 7 + direction[1]


    # normalise optimal move, NEEDS IMPROVEMENT
    if direction[0] !=0:
        direction[0] = int(direction[0] / abs(direction[0]))

    if direction[1] !=0:
        direction[1] = int(direction[1] / abs(direction[1]))

    # if invalid direction, pick upwards or downwards
    if (direction[0] * direction[1]) > 0:
        direction[0] = 0
    

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


