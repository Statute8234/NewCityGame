import ursina
from ursina import *
from ursina.shaders import lit_with_shadows_shader
import Island, Menu

# Capital
class CapitalBuilding(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = (1,2,1)
        self.name = 'Capital'
        self.model = 'cube'
        self.texture = 'brick'
        self.color = color.red
        self.menu = Menu.CapitalMenu(self)

    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity == self:
            self.menu.menu.enabled = True

# building
class Building(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'cube'
        self.texture = 'white_cube'
        self.color = color.red
        self.shader = lit_with_shadows_shader

# place builiding
availible_spots = Island.availible_spots
def place_building(position):
    for item in availible_spots:
        if item[0] == position[0] and item[2] == position[2]:
            capital = CapitalBuilding(position=(item[0],item[1] + 1.5,item[2]))
