# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import math
import copy
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

    #blueHexes = check_grid(input, 'b')
    #redHexes = check_grid(input, 'r')
    valid_directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
    current_grid = {"blueHexes": check_grid(input, 'b'), "redHexes": check_grid(input, 'r')}
    list_of_moves = []
    counter = 0

    # loop while there are still blue hexes on grid
    while current_grid["blueHexes"]:
        print("\nNEW CYCLE\n")
        potential_moves = []
        shortest_distance = 1000

        # for all red hexes
        print(current_grid["redHexes"])
        for redHex in current_grid["redHexes"].keys():
            print(redHex)
            #generate a possible future state
            for direction in valid_directions:
                potential_moves.append(generateState(current_grid, redHex, direction))

        print(current_grid["redHexes"])
        # run a heuristic
        best_heuristic = [0, 1000]
        best_state = current_grid
        for state in potential_moves:
    
            state_heuristic = state[2]

            # converts less hexes, ignore
            if state_heuristic[0] < best_heuristic[0]:
                continue

            # more hexes to convert
            if state_heuristic[0] > best_heuristic[0] or state_heuristic[1] < best_heuristic[1]:
                best_heuristic = state_heuristic
                best_state = state
                continue
          
        
        list_of_moves.append(best_state[1])

        current_grid = best_state[0]
 

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...


    return list_of_moves

def heuristic(state_under_consideration: dict[dict, dict]):

    shortest_distance = 1000
    for blueHex in state_under_consideration["blueHexes"].keys():
        for redHex in state_under_consideration["redHexes"].keys():

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

            distance = math.dist(blueHex, redHex)

            # the shortest possible distance
            if distance == 0:
                return distance

            if distance < shortest_distance:
                shortest_distance = distance


    return shortest_distance
    

    
def generateState(current_grid: dict[dict, dict], redHex: tuple, direction: tuple):

    heuristic_result = [0, 1000]
    new_state = copy.deepcopy(current_grid)

    for power in range(1, current_grid["redHexes"][redHex][1] + 1):

        r_new = (redHex[0] + direction[0] * power) % 7
        q_new = (redHex[1] + direction[1] * power) % 7

        # remove a blue hex
        if (r_new, q_new) in new_state["blueHexes"]:
            heuristic_result[0] += 1
            new_state["redHexes"].update({ (r_new, q_new): (new_state["blueHexes"][(r_new, q_new)])} )
            new_state["blueHexes"].pop((r_new, q_new), None)
   
        # update a red hex
        if (r_new, q_new) in new_state["redHexes"]:

            if new_state["redHexes"][(r_new, q_new)][1] < 6:
                new_state["redHexes"].update({(r_new, q_new) : ('r', new_state["redHexes"][(r_new, q_new)][1] + 1)})
            else:
                new_state["redHexes"].pop((r_new, q_new), None)
        else:
            new_state["redHexes"].update({(r_new, q_new) : ('r', 1)})

    new_state["redHexes"].pop((redHex))

    if heuristic_result[0] == 0:
        heuristic_result[1] = heuristic(new_state)

    if not new_state["redHexes"]:
        return None
    
    return (new_state, redHex + direction, heuristic_result)


# checks the current game state, returns dict of opponent tiles. If none, returns empty dict.
# takes dictionary of (r,q):(player,k) and colour 
def check_grid(input: dict[tuple, tuple], colour):
    tmp = dict()
    for key, value in input.items():
        if colour in value:
            tmp[key] =  value
    return tmp

