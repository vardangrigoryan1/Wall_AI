from vectorized_pathfinding import _neighbors_of, _reconstruct

#NO HEURISTIC

def _dfs(grid, start, goal, hazards_positions):
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        current = stack.pop()
        if current == goal:
            return _reconstruct(came_from, current)

        for next_x, next_z, _cost in _neighbors_of(grid, *current, hazards_positions):
            next_cell = (next_x, next_z) #AFTER SENT
            if next_cell not in visited:
                visited.add(next_cell)
                came_from[next_cell] = current
                stack.append(next_cell)
    return None

#©Vardan Grigoryan
