from ursina import *
import environmental_mechanics
import clustering

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


def run_clustering_button():
    environmental_mechanics.set_algorithm("astar")
    environmental_mechanics.game_started = True
    environmental_mechanics.player.enabled = True

    mouse.locked = True
    mouse.visible = False

    destroy(menu_root)

    from environmental_mechanics import grid, walle, debris_positions, hazards_positions
    agent_position = environmental_mechanics.cell(walle.position)
    clustering.run_clustering(grid, agent_position, debris_positions, hazards_positions=hazards_positions)




def create_menu():
    global menu_root
    menu_root = Entity(parent=camera.ui)

    mouse.locked = False
    mouse.visible = True

    Text(parent=menu_root,
         text="Choose Pathfinding Algorithm :))",
         origin=(0,0),
         y=0.35-0.04,
         scale=2)
    
    Button(parent=menu_root,
           text="A*",
           scale=(0.3,0.1),
           x=-0.2, y=0.2-0.04,
           on_click=Func(choose, "astar"))
    
    Button(parent=menu_root,
           text="BFS",
           scale=(0.3,0.1),
           x=0.2, y=0.2-0.04,
           on_click=Func(choose, "bfs"))

    Button(parent=menu_root,
           text="UCS",
           scale=(0.3,0.1),
           x=-0.2, y=0.05-0.04,
           on_click=Func(choose, "ucs"))
    
    Button(parent=menu_root,
           text="DFS",
           scale=(0.3,0.1),
           x=0.2, y=0.05-0.04,
           on_click=Func(choose, "dfs"))

    Button(parent=menu_root,
           text="Greedy",
           scale=(0.3,0.1),
           x=0, y=-0.1-0.04, 
           on_click=Func(choose, "greedy"))


    Button(parent=menu_root,
           text="Clustering",
           scale=(0.3,0.1),
           x=0, y=-0.25-0.04,
           on_click=Func(run_clustering_button))

#©Vardan Grigoryan
