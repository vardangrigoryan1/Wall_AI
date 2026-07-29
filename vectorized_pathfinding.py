### MOVEMENT ### MOVEMENT ### MOVEMENT ###
NEIGHBORS = [
             (1, 0),
             (-1, 0),
             (0, 1),
             (0, -1),
             (1, 1),
             (1, -1),
             (-1, 1),
             (-1, -1)
            ]
### MOVEMENT ### MOVEMENT ### MOVEMENT ###


### <-----------------------------> ###
STRAIGHT_COST = 1.0
DIAGONAL_COST = 1.4142135623730951  #root(2)

ELECTRICAL_COST = 10000
PIT_COST = 1000
### <-----------------------------> ###


### <-----------------------------> ###
def parse_maze(maze, wall="1", debris="O", plant="P", base="B", walle="W", pit="X", electrical="E"):
    height = len(maze)
    width = max(len(row) for row in maze)

    grid = [[1] * width for _ in range(height)]
    debris_positions = []
    plant_position = None
    base_position = None
    walle_position = None
    hazards_positions = {}

    for z, row in enumerate(maze):
        for x in range(width):
            symb = row[x] if x < len(row) else wall
            if symb == wall:
                grid[z][x] = 1
            else:
                grid[z][x] = 0
                if symb == debris:
                    debris_positions.append((x, z))
                elif symb == plant:
                    plant_position = (x, z)
                elif symb == base:
                    base_position = (x, z)
                elif symb == walle:
                    walle_position = (x, z)
                elif symb == pit:
                    hazards_positions[(x, z)] = "pit"
                elif symb == electrical:
                    hazards_positions[(x, z)] = "electrical"

    return grid, debris_positions, plant_position, base_position, walle_position, hazards_positions
### <-----------------------------> ###


### <-----------------------------> ###
def _walkable(grid, x, z):
    height = len(grid)
    width = len(grid[0])

    inside_map = (
        0 <= x < width
        and
        0 <= z < height)
    not_wall = (
        grid[z][x] == 0)

    is_walkable = inside_map and not_wall
    return is_walkable
### <-----------------------------> ###


### <-----------------------------> ###
def _diagonal_is_blocked(grid, x, z, move_x, move_z): #all are current xurrent_x, zurrent
    horizontal_cell = (x + move_x, z)
    vertical_cell = (x, z + move_z)

    horizontal_is_walkable = _walkable(grid, horizontal_cell[0], horizontal_cell[1])
    vertical_is_walkable = _walkable(grid, vertical_cell[0], vertical_cell[1])

    is_blocked = not horizontal_is_walkable or not vertical_is_walkable
    return is_blocked
### <-----------------------------> ###


def _neighbors_of(grid, x, z, hazards_positions):
    for move_x, move_z in NEIGHBORS:
        new_x = x + move_x
        new_z = z + move_z

        if not _walkable(grid, new_x, new_z):
            continue

        is_diagonal = (move_x != 0 and move_z != 0)
        if (is_diagonal #if it is diagonal, only check diagonals
            and
            _diagonal_is_blocked(grid, x, z, move_x, move_z)):
            continue

        if is_diagonal:
            cost = DIAGONAL_COST
        else: #left right up down
            cost = STRAIGHT_COST

        #Hazard penalty
        if (new_x, new_z) in hazards_positions:
            hazard_type = hazards_positions[(new_x, new_z)]

            if hazard_type == "pit":
                cost += PIT_COST
            elif hazard_type == "electrical":
                cost += ELECTRICAL_COST

        yield new_x, new_z, cost
### <-----------------------------> ###


### <-----------------------------> ###
def _reconstruct(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
### <-----------------------------> ###


### <-----------------------------> ###
from astar import _astar
from bfs import _bfs
from dfs import _dfs
_ALGORITHMS = {
    "astar": _astar,
    "bfs": _bfs,
    "dfs": _dfs,
}

def find_path(grid, start, goal, algorithm="astar", hazards_positions=None):
    if algorithm not in _ALGORITHMS:
        raise ValueError(f"Unknown algorithm '{algorithm}'. Choose from {list(_ALGORITHMS)}")

    if not (_walkable(grid, *start) and _walkable(grid, *goal)):
        return None
    if start == goal:
        return [start]

    hazards_positions = hazards_positions or {}
    return _ALGORITHMS[algorithm](grid, start, goal, hazards_positions)
### <-----------------------------> ###

#©Vardan Grigoryan
