from ursina import *
import environmental_mechanics

menu_root = None

#for e in scene.entities:
#    e.enabled = False
environmental_mechanics.player.enabled = False

def choose(algo):
    environmental_mechanics.set_algorithm(algo)
    environmental_mechanics.game_started = True

    #for e in scene.entities:
    #    e.enabled = True
    environmental_mechanics.player.enabled = True
    
    mouse.locked = True
    mouse.visible = False

    destroy(menu_root)


def create_menu():
    global menu_root
    menu_root = Entity(parent=camera.ui)

    mouse.locked = False
    mouse.visible = True

    Text(parent=menu_root,
         text="Choose Pathfinding Algorithm", origin=(0,0), y=0.35, scale=2)
    
    Button(parent=menu_root,
           text="A*",
           scale=(0.3,0.1),
           y=0.15,
           on_click=Func(choose, "astar"))
    
    Button(parent=menu_root,
           text="BFS",
           scale=(0.3,0.1),
           y=0,
           on_click=Func(choose, "bfs"))
    
    Button(parent=menu_root,
           text="DFS",
           scale=(0.3,0.1),
           y=-0.15,
           on_click=Func(choose, "dfs"))

    Button(parent=menu_root,
           text="Greedy",
           scale=(0.3,0.1),
           y=-0.3, 
           on_click=Func(choose, "greedy"))

#©Vardan Grigoryan
