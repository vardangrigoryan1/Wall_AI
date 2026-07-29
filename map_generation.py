from vectorized_pathfinding import parse_maze
from rmap_generation import I_want_to_create_a_random_map, generate_random_map

#"1" = wall (not walkable)
#"O" = debris (walkable, collectible, +1 point)
#" " = empty floor (walkable)
#"P" = plant (walkable, +5 points, must be delivered to the player)
#"X" = pit hazard (walkable, avoided by A*, costs points if crossed)
#"E" = electric hazard (walkable, avoided by A*, costs points if crossed)
#"B" = Base

maze = ["1111111111111111111111111111111111111111111111111111",
        "1   111111111111111111111         O                1",
        "1                                                  1",
        "1                                                  1",
        "1           111111111111111111111                  1",
        "1      O             111111111111111111111         1",
        "1                              1111                1",
        "1                             1111                 1",
        "1     W       O        E       1111                1",
        "1                              1111                1",
        "1                  1            1                  1",
        "1                  1    X       1        P         1",
        "1   B           1111           11                  1",
        "1                  1            1                  1",
        "1               1111           11                  1",
        "1111111111111111111111111111111111111111111111111111"]

if I_want_to_create_a_random_map is True:
        maze = generate_random_map()
elif I_want_to_create_a_random_map is False:
        maze = maze #pass

grid, debris_positions, plant_position, base_position, walle_position, hazards_positions = parse_maze(maze)

#©Vardan Grigoryan
