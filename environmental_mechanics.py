from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from map_generation import *
from heuristics import _manhattan_heuristic
from vectorized_pathfinding import find_path
from performance_measure import add_score, POINTS_DEBRIS, POINTS_PLANT, POINTS_HAZARD
from ursina.shaders import lit_with_shadows_shader

game_started = False
def set_algorithm(algorithm):
    global ALGORITHM
    ALGORITHM = algorithm
    print("Using algorithm:", ALGORITHM)


### <----------------------------------- WORLD ----------------------------------> ###
sky = Sky(texture="sky_sunset")
walle_voice = Audio("sounds/walle_voice.mp3", autoplay=False)
soundtrack = Audio("sounds/soundtrack.mp3", autoplay=False)
soundtrack.play()

ground = Entity(model="plane",
                 scale=(100, 1, 100),
                 position=(0, 0.01, 0),
                 texture="textures/ground.jpg",
                 texture_scale=(36, 36),
                 collider="box",
                 double_sided=True,
                 shader=lit_with_shadows_shader,
                 color=color.white)

debris_entities = {}
hazard_entities = {}
for z in range(len(maze)):
    row = maze[z]
    for x in range(len(row)):
        ch = row[x] if x < len(row) else "1"

        if ch == "1":
            Entity(model="cube",
                   scale=(1, 10/2, 1),
                   position=(x, 5/2, z),
                   texture="textures/wall.jpg",
                   texture_scale=(1/3, 10/3),
                   collider="box",
                   shader=lit_with_shadows_shader)

        elif ch == "O":
            debris_model = random.choice([ ("objects/debris1.glb", 1, -0.04), ("objects/debris2.glb", 0.28, 0.2) ])
            debris_entities[(x, z)] = Entity(model=debris_model[0],
                                              scale=debris_model[1],
                                              position=(x, debris_model[2], z),
                                              collider="box")
                                              #color=color.brown)

        elif ch == "X":
            hazard_entities[(x, z)] = Entity(model="cube",
                                              scale=(1, 0.05, 1),
                                              position=(x, 0.0, z),
                                              color=color.black)

        elif ch == "E":
            hazard_entities[(x, z)] = Entity(model="electrical.glb",
                                              scale=0.07,
                                              position=(x, 0.0, z),
                                              shader=lit_with_shadows_shader)
                                              #color=color.yellow)

plant_entity = Entity(model="plant_rot.glb",
                      scale=0.09,
                      position=(plant_position[0], -0.04, plant_position[1]),
                      collider="box")
                      #color=color.green)

walle = Entity(#model="objects/wall-e.glb",
               model="objects/wall_e_rot.glb",
               scale=0.6,
               #color=color.red,
               position=(1, 0, 1),
               shader=lit_with_shadows_shader)

### <----------------------------------- WORLD ----------------------------------> ###

### <------------ PLAYER + LIGHTS ------------> ###
player = FirstPersonController()
player_model = Entity(parent=player,
               model="objects/eva_rot.glb",
               scale=0.6,
               position=(0, 0.3, -0.41),
               shader=lit_with_shadows_shader)
player.position = (3, 10, 15)
player.camera_pivot.y = 1.4

scene.fog_density = (10, 400)
sun = DirectionalLight()
sun.look_at(Vec3(-1, -1, -1))
sun.color = color.white
#sun._light.show_frustum()
### <------------ PLAYER + LIGHTS ------------> ###

### <---- CONFIGURATION CHARACTERISTICS (state) ----> ###
WALLE_SPEED = 4.0
DELIVERY_DISTANCE = 1.5
REPATH_INTERVAL = 0.4

current_target_is_plant = False
carrying_plant =          False
plant_delivered =         False

returning_to_base =       False
at_base =                 False

current_path =            []

chase_timer =             0.0
wait_timer =              0.0
WAIT_BEFORE_RETURN =      3.0
### <---- CONFIGURATION CHARACTERISTICS (state) ----> ###

### <------------------------ VECTORIZED_PATHFINDING_2.0_HELPER  ------------------------> ###
def cell(pos):
    return (round(pos.x), round(pos.z))

# poxarinel em _manhattan_heuristic ov heuristics.py-ic
# def manhattan(a, b):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pick_next_target():
    here = cell(walle.position)
    minigoal_target_candidates = []

    minigoal_target_candidates += list(debris_entities.keys())
    if (plant_position is not None 
        and
        plant_delivered is False
        and
        carrying_plant is False):
        minigoal_target_candidates.append(plant_position)

    if len(minigoal_target_candidates) == 0:
        return None

    def distance(candidate):
        return _manhattan_heuristic(here, candidate)
    minigoal_target_candidates.sort(key=distance)

    return minigoal_target_candidates[0]


def start_new_path():
    global current_path, current_target_is_plant
    here = cell(walle.position)
    current_mini_target = pick_next_target()

    if current_mini_target is None:
        current_path = []
        return

    if current_mini_target == plant_position and carrying_plant is False:
        current_target_is_plant = True

    path = find_path(grid, start=here, goal=current_mini_target, algorithm=ALGORITHM, hazards_positions=hazards_positions)
    if len(path) != 0:
        current_path = path[1:]   #drop starting cell
    else: #len(path) == 0:
        current_path = []


def start_chase_path():
    global current_path
    here = cell(walle.position)
    player_cell = cell(player.position)
    
    path = find_path(grid, start=here, goal=player_cell, algorithm=ALGORITHM, hazards_positions=hazards_positions)
    if len(path) != 0:
        current_path = path[1:]   #drop starting cell
    else: #len(path) == 0:
        current_path = []
### <------------------------ VECTORIZED_PATHFINDING_2.0_HELPER  ------------------------> ###



### <------------------------ MAIN URS. GAME LOOP  ------------------------> ###
def update():
    global current_path, carrying_plant, plant_delivered
    global chase_timer
    global returning_to_base, at_base, wait_timer
    if not game_started:
        return

    #if at_base:
    #   return  #Walle stands still permanently once back at base


    ### <---------------------------> ###
    if returning_to_base is False and plant_delivered is False and len(current_path) == 0:
        start_new_path()
    ### <---------------------------> ###

    ### <---------------------------> ###
    if carrying_plant is True:
        plant_entity.parent = walle
        plant_entity.position = Vec3(0.4, 0.1, 0.8) #CHASE ANELU PAHIN WALLE MOTINY

        chase_timer += time.dt
        if chase_timer >= REPATH_INTERVAL:
            chase_timer = 0.0
            start_chase_path()

        if distance(walle.position, player.position) <= DELIVERY_DISTANCE:
            carrying_plant = False
            plant_delivered = True
            walle_voice.play()
            plant_entity.parent = player
            plant_entity.position = Vec3(0.4, 0.3, 0.6) #IM DZERQUM LINELY
            plant_entity.rotation_y = -10
            plant_entity.collider = None
            add_score(POINTS_PLANT, "plant delivered to player")
            return

        if not current_path:
            return  #nopath found this tick, will retry next chase interval
    ### <---------------------------> ###

    ### <---------------------------> ###
    if plant_delivered is True and returning_to_base is False:
        wait_timer += time.dt
        if wait_timer >= WAIT_BEFORE_RETURN:
            returning_to_base = True
            here = cell(walle.position)
            base = base_position

            path = find_path(grid, start=here, goal=base, algorithm=ALGORITHM, hazards_positions=hazards_positions)
            if len(path) != 0:
                current_path = path[1:]   #drop starting cell
            else: #len(path) == 0:
                current_path = []
        return  # stand still while waiting
    ### <---------------------------> ###

    ### <---------------------------> ###
    # --- Returning to base: check arrival once path is exhausted ---
    if returning_to_base is True and len(current_path) == 0:
        at_base = True
        print("Walle is back at base!")
        return
    ### <---------------------------> ###
    ### <----------------------------------------------------------------> ###
    ### <----------------------------------------------------------------> ###
    ### <---------------------------> ###
    next_cell = current_path[0]
    target_pos = Vec3(next_cell[0], 0, next_cell[1])

    direction = target_pos - walle.position
    direction.y = 0
    dist = direction.length()
    step = WALLE_SPEED * time.dt

    if dist <= step:
        walle.position = target_pos
        current_path.pop(0)

        if returning_to_base is False and next_cell in debris_entities:
            destroy(debris_entities.pop(next_cell))
            add_score(POINTS_DEBRIS, f"debris at {next_cell}")

        if returning_to_base is False and next_cell in hazards_positions:
            add_score(POINTS_HAZARD, f"hazard at {next_cell}")

        if current_target_is_plant and next_cell == plant_position and carrying_plant is False and plant_delivered is False:
            carrying_plant = True
            current_path = []
            chase_timer = REPATH_INTERVAL  # force an immediate chase path next tick
            print("Picked up the plant, chasing the player...")
    else:
        walle.position += direction.normalized() * step
        walle.look_at(Vec3(target_pos.x, walle.y, target_pos.z))
### <------------------------ MAIN URS. GAME LOOP  ------------------------> ###


### <----------- KEYBOARD  -----------> ###
def input(key):
    if key == "escape":
        quit()
    if held_keys["shift"]:
        player.speed = 10
    else:
        player.speed = 5
    if held_keys["space"]:
        player.jump()
### <----------- KEYBOARD  -----------> ###

#©Vardan Grigoryan
