from collections import deque

#NO HEURISTIC
from vectorized_pathfinding import _neighbors_of, _reconstruct

def _bfs(grid, start, goal, hazards_positions):
    frontier = deque([start])
    came_from = {}
    visited = {start}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            return _reconstruct(came_from, current)

        for next_x, next_z, _cost in _neighbors_of(grid, *current, hazards_positions):
            next_cell = (next_x, next_z)
            if next_cell not in visited:
                visited.add(next_cell)
                came_from[next_cell] = current
                frontier.append(next_cell)
    return None

#©Vardan Grigoryan