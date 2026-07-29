import heapq
 
from heuristics import _octile_heuristic, _manhattan_heuristic, _euclidean_heuristic, _chebyshev_heuristic
from vectorized_pathfinding import _neighbors_of, _reconstruct

HEURISTICS = {
    "octile": _octile_heuristic,
    "manhattan": _manhattan_heuristic,
    "euclidean": _euclidean_heuristic,
    "chebyshev": _chebyshev_heuristic,
}
heuristic = HEURISTICS["octile"]

def _greedy(grid, start, goal, hazards_positions):
    frontier = [(heuristic(start, goal), start)]

    came_from = {}
    #g = {start: 0}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            return _reconstruct(came_from, current)

        if current in visited:
            continue

        visited.add(current)

        for next_x, next_z, cost in _neighbors_of(grid, *current, hazards_positions):
            next_cell = (next_x, next_z)

            #g(child) via this node = g(n) + c(n, a, child)
            #new_g = g[current] + cost

            ### <------------------------> ###
            if next_cell == start:
                continue
            ### <------------------------> ###

            if next_cell not in came_from:                      #if new_g < g.get(next_cell, float("inf")):
                                                                #g[next_cell] = new_g
                came_from[next_cell] = current
                f = heuristic(next_cell, goal)                  #f = new_g + _octile_heuristic(next_cell, goal)
                heapq.heappush(frontier, (f, next_cell))
    return None

#©Vardan Grigoryan