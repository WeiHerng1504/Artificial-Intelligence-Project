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

    validDirections = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
    currentGrid = {"blueHexes": check_grid(input, 'b'), "redHexes": check_grid(input, 'r')}

    # state format
    # state = {gridLayout, previousMoves, heuristicResults, gameEnded}
    startingState = {"gridLayout": currentGrid, "previousMoves": [], 
                     "heuristicResult": [], "gameEnded": False}

    bestStates = [startingState]
    solution = False

    while not solution:
        
        potentialMoves = []

        for state in bestStates:
            # for all red hexes
            for redHex in state["gridLayout"]["redHexes"]:
                #generate a possible future state
                for direction in validDirections:
                    newState = generateState(state, redHex, direction)
                    if newState:
                        potentialMoves.append(newState)


        # run a heuristic comparison
        # heuristic has two components, 
        # first item is hexes converted, 
        # second item is shortest straight line distance
        # we prioritize first item

        # placeholder values to be replaced
        bestHeuristic = [0, 1000]

        for state in potentialMoves:
            # solution found
            if state["gameEnded"]:
                solution = state["previousMoves"]
                break

            # converts more hexes
            if state["heuristicResult"][0] > bestHeuristic[0]:
                bestHeuristic = state["heuristicResult"]
                continue

            # shorter distance
            if state["heuristicResult"][0] == bestHeuristic[0] and state["heuristicResult"][1] < bestHeuristic[1]:
                bestHeuristic = state["heuristicResult"]


        # keeping only desirable nodes
        if not solution:
            bestStates = [state for state in potentialMoves if state["heuristicResult"] == bestHeuristic]


        
    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...


    return solution

# Estimates the shortest straight line distance between a blue and red hexagon
# Takes a grid layout as input.
# Returns the shortest distance between two opposing hexes
def heuristic(layout: dict[dict, dict]):

    # placeholder value to be replaced
    shortestDistance = 1000
 
    for blueHex in layout["blueHexes"].keys():
        for redHex in layout["redHexes"].keys():

             # manhattan distance with relative direction
            manDist = [blueHex[0] - redHex[0], blueHex[1] - redHex[1]]

            # check if wrapping is closer
            for axis in range(len(manDist)):
                if abs(manDist[axis]) > 3:
                    if manDist[axis] < 0:
                        manDist[axis] = manDist[axis] + 7
                    else:
                        manDist[axis] = manDist[axis] - 7

            # vertical 
            if manDist[0] != 0 and manDist[1] != 0 and manDist[0] / manDist[1] == -1:
                distance = abs(manDist[0])
            # closer vertically compared to horizontally
            elif manDist[0] != 0 and manDist[1] != 0 and manDist[0] / manDist[1] < 0:
                distance = math.sqrt( math.pow(manDist[0], 2) + math.pow(manDist[1], 2) - 
                            2*abs(manDist[0])*abs(manDist[1])*math.cos(1/3 * math.pi))
            # general case
            else:
                distance = math.hypot(abs(manDist[0]), abs(manDist[1]))

            # shorter, keep track
            if distance < shortestDistance:
                shortestDistance = distance

    return shortestDistance
    

# Simulate a move. 
# Takes a state, red hexagon location and movement direction as input.
# Returns the simulated move as a new state
def generateState(predecessor: dict[dict, list, list, bool], 
                  redHex: tuple, direction: tuple):

    # state format
    # state = {gridLayout, previousMoves, heuristic_results, gameEnded}

    # initialize with first component of heuristic 
    heuristicResult = [0]

    newState = copy.deepcopy(predecessor)
    newGrid = newState["gridLayout"]
    
    for power in range(1, newGrid["redHexes"][redHex][1] + 1):

        r_new = (redHex[0] + direction[0] * power) % 7
        q_new = (redHex[1] + direction[1] * power) % 7

        # remove a blue hex
        if (r_new, q_new) in newGrid["blueHexes"]:
            heuristicResult[0] += 1
            newGrid["redHexes"].update({(r_new, q_new): 
                            (newGrid["blueHexes"][(r_new, q_new)])})
            newGrid["blueHexes"].pop((r_new, q_new), None)
   
        # update a red hex
        if (r_new, q_new) in newGrid["redHexes"]:
            if newGrid["redHexes"][(r_new, q_new)][1] < 6:
                newGrid["redHexes"].update({(r_new, q_new): 
                            ('r', newGrid["redHexes"][(r_new, q_new)][1] + 1)})
            else:
                newGrid["redHexes"].pop((r_new, q_new), None)
        else:
            newGrid["redHexes"].update({(r_new, q_new) : ('r', 1)})

    # remove starting hex
    newGrid["redHexes"].pop((redHex))

    # update heuristic
    heuristicResult.append(heuristic(newGrid))

    # state with no redhexes, avoid
    if not newGrid["redHexes"]:
        return None

    # terminal state?
    if not newGrid["blueHexes"]:
        gameEnded = True
    else:
        gameEnded = False

    newState["previousMoves"].append(redHex + direction)

    return {"gridLayout": newGrid, "previousMoves": newState["previousMoves"], 
            "heuristicResult": heuristicResult, "gameEnded": gameEnded}


# checks the current game state, returns dict of opponent tiles. If none, returns empty dict.
# takes dictionary of (r,q):(player,k) and colour 
def check_grid(input: dict[tuple, tuple], colour):
    tmp = dict()
    for key, value in input.items():
        if colour in value:
            tmp[key] =  value
    return tmp


