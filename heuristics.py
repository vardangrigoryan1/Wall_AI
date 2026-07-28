from vectorized_pathfinding import DIAGONAL_COST

def _octile_heuristic(a, b):
    move_x = abs(a[0] - b[0])
    move_z = abs(a[1] - b[1])
    return (move_x + move_z) + (DIAGONAL_COST - 2) * min(move_x, move_z)

def _manhattan_heuristic(a, b):
    move_x = abs(a[0] - b[0])
    move_z = abs(a[1] - b[1])
    return move_x + move_z

import math
def _euclidean_heuristic(a, b):
    move_x = abs(a[0] - b[0])
    move_z = abs(a[1] - b[1])
    return math.sqrt(move_x**2 + move_z**2)

def _chebyshev_heuristic(a, b):
    move_x = abs(a[0] - b[0])
    move_z = abs(a[1] - b[1])
    return max(move_x, move_z)

#©Vardan Grigoryan