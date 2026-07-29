from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()
window.title = "Wall-AI"
window.cog_button.enabled = False
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
