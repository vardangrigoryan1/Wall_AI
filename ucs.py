import heapq
 
#from heuristics import _octile_heuristic
from vectorized_pathfinding import _neighbors_of, _reconstruct

def _ucs(grid, start, goal, hazards_positions):
    frontier = [(0, start)]

    came_from = {}
    g = {start: 0}
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
            new_g = g[current] + cost

            if new_g < g.get(next_cell, float("inf")):
                g[next_cell] = new_g
                came_from[next_cell] = current
                f = new_g                                       # + _octile_heuristic(next_cell, goal)
                heapq.heappush(frontier, (f, next_cell))
    return None

#©Vardan Grigoryan