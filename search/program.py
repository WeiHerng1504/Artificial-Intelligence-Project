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

    # shortest_distance = 0
    # for every blue hex 
    #      for every red hex

    #         if heuristic(blue, red) <   

    ## make the move

    

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


# calculates and returns straight line distance
def heuristic(firstHex: tuple, secondHex: tuple):

    distance = math.dist(firstHex - secondHex)
    
    return distance


# checks the current game state, returns list of opponent tiles. If none, returns empty list.
# takes dictionary of (r,q):(player,k) and colour 
def check_grid(input: dict[tuple, tuple], colour):
    tmp = list()
    for key,value in input.items():
        if colour in value:
            tmp.append(key+value)
    return tmp