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

    valid_directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
    current_grid = {"blueHexes": check_grid(input, 'b'), "redHexes": check_grid(input, 'r')}

    # state format
    # state = {gridLayout, previousMoves, heuristicResults, gameEnded}
    starting_state = {"gridLayout": current_grid, "previousMoves": [], "heuristicResult": [], "gameEnded": False}

    best_states = [starting_state]
    solution = False

    while not solution:
        
        potential_moves = []

        for state in best_states:
            # for all red hexes
            for redHex in state["gridLayout"]["redHexes"]:
                #generate a possible future state
                for direction in valid_directions:
                    new_state = generateState(state, redHex, direction)
                    if new_state:
                        potential_moves.append(new_state)


        # run a heuristic comparison
        # heuristic has two components, first item is hexes converted, 
        # second item is shortest straight line distance
        bestHeuristic = [0, 1000]
        for state in potential_moves:

            if state["gameEnded"]:
                solution = state["previousMoves"]
                break

       
            # converts more
            if state["heuristicResult"][0] > bestHeuristic[0]:
                bestHeuristic = state["heuristicResult"]
                continue

            # shorter distance

            if state["heuristiResult"][0] == bestHeuristic[0] and state["heuristicResult"][1] < bestHeuristic[1]:
                bestHeuristic = state["heuristicResult"]


        # keeping only desirable nodes
        if not solution:
            best_states = [state for state in potential_moves if state["heuristicResult"] == bestHeuristic]


        
    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...


    return solution

# straight line distance
def heuristic(state_under_consideration: dict[dict, dict]):

    shortest_distance = 1000
 
    for blueHex in state_under_consideration["blueHexes"].keys():
        for redHex in state_under_consideration["redHexes"].keys():

             # directions to move, normalized
            man_dist = [abs(blueHex[0] - redHex[0]), abs(blueHex[1] - redHex[1])]

            # check if wrapping is closer
            if man_dist[0] > 3:
                man_dist[0] = abs(man_dist[0] - 7)

            if man_dist[1] > 3:
                man_dist[1] = abs(man_dist[1] - 7)

            # vertical 
            if man_dist[0] != 0 and man_dist[1] != 0 and man_dist[0] / man_dist[1] == -1:
                distance = abs(man_dist[0])
            # general case
            else:
                distance = math.hypot(abs(man_dist[0]), abs(man_dist[1]))

            if distance > shortest_distance:
                continue

            if distance < shortest_distance:
                shortest_distance = distance


    return shortest_distance
    

    
def generateState(predecessor: dict[dict, list, list, bool], redHex: tuple, direction: tuple):

    # state format
    # state = {gridLayout, previousMoves, heuristic_results, gameEnded}

    heuristic_result = [0]
    new_state = copy.deepcopy(predecessor)
    new_grid = new_state["gridLayout"]
    
    for power in range(1, new_grid["redHexes"][redHex][1] + 1):

        r_new = (redHex[0] + direction[0] * power) % 7
        q_new = (redHex[1] + direction[1] * power) % 7

        # remove a blue hex
        if (r_new, q_new) in new_grid["blueHexes"]:
            heuristic_result[0] += 1
            new_grid["redHexes"].update({ (r_new, q_new): (new_grid["blueHexes"][(r_new, q_new)])} )
            new_grid["blueHexes"].pop((r_new, q_new), None)
   
        # update a red hex
        if (r_new, q_new) in new_grid["redHexes"]:

            if new_grid["redHexes"][(r_new, q_new)][1] < 6:
                new_grid["redHexes"].update({(r_new, q_new) : ('r', new_grid["redHexes"][(r_new, q_new)][1] + 1)})
            else:
                new_grid["redHexes"].pop((r_new, q_new), None)
        else:
            new_grid["redHexes"].update({(r_new, q_new) : ('r', 1)})

    # remove starting hex
    new_grid["redHexes"].pop((redHex))

    # LOOK AT THIS!!!
    heuristic_result.append(heuristic(new_grid))

    # state with no redhexes, avoid
    if not new_grid["redHexes"]:
        return None

    if not new_grid["blueHexes"]:
        gameEnded = True
    else:
        gameEnded = False


    new_state["previousMoves"].append(redHex + direction)

    return {"gridLayout": new_grid, "previous_moves": new_state["previousMoves"], "heuristic_result": heuristic_result, "gameEnded": gameEnded}


# checks the current game state, returns dict of opponent tiles. If none, returns empty dict.
# takes dictionary of (r,q):(player,k) and colour 
def check_grid(input: dict[tuple, tuple], colour):
    tmp = dict()
    for key, value in input.items():
        if colour in value:
            tmp[key] =  value
    return tmp


