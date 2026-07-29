import random
from collections import deque
from vectorized_pathfinding import NEIGHBORS


def find_reachable_cells(maze, start):
   
    number_of_rows = len(maze)
    number_of_columns = len(maze[0])

    cells_to_check = deque([start])
    reachable_cells = {start}

    while cells_to_check:
        current_x, current_z = cells_to_check.popleft()

        for change_x, change_z in NEIGHBORS:
            next_x = current_x + change_x
            next_z = current_z + change_z

            if not (0 <= next_x < number_of_columns
                    and
                    0 <= next_z < number_of_rows):
                continue

            if maze[next_z][next_x] == "1":
                continue

            is_diagonal = change_x != 0 and change_z != 0

            if is_diagonal:
                horizontal_cell_is_wall = maze[current_z][next_x] == "1"
                vertical_cell_is_wall = maze[next_z][current_x] == "1"

                if horizontal_cell_is_wall or vertical_cell_is_wall:
                    continue

            next_cell = (next_x, next_z)

            if next_cell not in reachable_cells:
                reachable_cells.add(next_cell)
                cells_to_check.append(next_cell)
    return reachable_cells


def generate_random_map(rows=23, columns=52, wall_probability=0.20, debris_count=3, pit_count=3, electrical_count=3):
    debris_count = max(3, debris_count)

    while True:
        maze = []
        for z in range(rows):
            new_row = []
            for x in range(columns):
                is_border = (z == 0
                             or
                             x == 0
                             or
                             z == rows - 1
                             or
                             x == columns - 1)

                if is_border:
                    new_row.append("1")
                elif random.random() < wall_probability:
                    new_row.append("1")
                else:
                    new_row.append(" ")

            maze.append(new_row)

        walle_start = (1, 1)
       #making sure Walle can move
        starting_area = [
            (1, 1),
            (2, 1),
            (1, 2),
            (2, 2)
        ]

        for x, z in starting_area:
            maze[z][x] = " "

        reachable_cells = find_reachable_cells(maze, walle_start)
        available_cells = list(reachable_cells - set(starting_area))
        number_of_objects = (1 + 1 + debris_count + pit_count + electrical_count)

        #generating new map if there is no enough space
        if len(available_cells) < number_of_objects:
            continue

        selected_cells = random.sample(available_cells, number_of_objects)
        current_index = 0

        #we need exactly one base
        base_x, base_z = selected_cells[current_index]
        maze[base_z][base_x] = "B"
        current_index += 1

        #we need exactly one plant
        plant_x, plant_z = selected_cells[current_index]
        maze[plant_z][plant_x] = "P"
        current_index += 1
    
        #we need zibiliks
        for _ in range(debris_count):
            debris_x, debris_z = selected_cells[current_index]
            maze[debris_z][debris_x] = "O"
            current_index += 1

        #we need pits
        for _ in range(pit_count):
            pit_x, pit_z = selected_cells[current_index]
            maze[pit_z][pit_x] = "X"
            current_index += 1

        #we need electrical
        for _ in range(electrical_count):
            electrical_x, electrical_z = selected_cells[current_index]
            maze[electrical_z][electrical_x] = "E"
            current_index += 1

        maze[walle_start[1]][walle_start[0]] = "W"

        return ["".join(row) for row in maze]

I_want_to_create_a_random_map = False

#©Vardan Grigoryan