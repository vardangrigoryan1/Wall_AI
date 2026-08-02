from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

#app = Ursina()
#window.title = "Wall-AI"
app = Ursina(title="Wall-AI - V.G.") #AFTER SENT
window.cog_button.enabled = False
window.entity_counter.enabled = False #AFTER SENT
window.collider_counter.enabled = False #AFTER SENT
EditorCamera()

import environmental_mechanics
import menu

menu.create_menu()

def update():
    environmental_mechanics.update()
def input(key):
    environmental_mechanics.input(key)

app.run()

#©Vardan Grigoryan
