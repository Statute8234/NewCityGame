import ursina
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.shaders import lit_with_shadows_shader
from math import radians, cos, sin
# ground
class Ground(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'cube'
        self.texture = "grass"
        self.color = color.green
        self.shader = lit_with_shadows_shader
        self.current_season = None
    
    def change(self, current_season):
        if self.current_season != current_season:
            self.texture = "grass"
            if current_season == 'spring':
                self.color = color.lime
            if current_season == 'summer':
                self.color = color.green
            if current_season == 'autumn':
                self.color = color.orange
            if current_season == 'winter':
                self.texture = "white_cube"
                self.color = color.white

# dome
class Dome(Entity):
    def __init__(self, subdivisions = 10, radius = 6):
        super().__init__()
        self.parent = scene
        self.model = self.create_dome(subdivisions, radius)
        self.texture = 'white_cube'
        self.scale = radius
        self.color = color.rgba(0,255,255,0.2)
        self.shader = lit_with_shadows_shader

    def create_dome(self, subdivisions, radius):
        verts = []
        tris = []

        for i in range(subdivisions + 1):
            for j in range(subdivisions + 1):
                theta = i / subdivisions * pi / 2
                phi = j / subdivisions * pi * 2
                x = radius * sin(theta) * cos(phi)
                y = radius * cos(theta)
                z = radius * sin(theta) * sin(phi)
                verts.append((x, y, z))
        
        for i in range(subdivisions):
            for j in range(subdivisions):
                v1 = i * (subdivisions + 1) + j
                v2 = v1 + (subdivisions + 1)
                v3 = v1 + 1
                v4 = v2 + 1
                if (i + j) % 2 == 0:
                    tris.extend([(v1, v2, v3), (v3, v2, v4)])
                else:
                    tris.extend([(v1, v2, v4), (v1, v4, v3)])

        normals = [Vec3(0, 1, 0) for _ in verts]
        uvs = [(i / subdivisions, j / subdivisions) for i in range(subdivisions + 1) for j in range(subdivisions + 1)]

        return Mesh(vertices=verts, triangles=tris, normals=normals, uvs=uvs)

# menu
class BuildingMenu(Entity):
    def __init__(self, building):
        super().__init__(parent=camera.ui)
        self.building = building
        self.building_menu = Entity(parent=self, enabled=True)
        self.job_menu = Entity(parent=self, enabled=False)
        self.jobsDropDown_Menu = None
        self.text_entities = []
        mouse.locked = False
        self.selected_job = None 
        
        # add test
        def addText():
            print(self.jobsDropDown_Menu.selected.text)
            # Clear all previous text entities
            for text_entity in self.text_entities:
                destroy(text_entity)
            self.text_entities.clear()

            # Ensure jobsDropDown_Menu is initialized and has buttons
            if self.selected_job is not None:
                self.building.holdInfo(self.selected_job)

                for label, position in self.building.fields.items():
                    text_entity = Text(label, parent=self, position=(-0.5, position[1]))
                    self.text_entities.append(text_entity)
        # menu
        def Remove():
            self.building_menu.disable()
            destroy(self.building)

        def Hide():
            self.building.buildingMenu.disable()
            if self.building.color != color.rgba(self.building.color[0], self.building.color[1], self.building.color[2], 0.1):
                self.building.color = color.rgba(self.building.color[0], self.building.color[1], self.building.color[2], 0.1)
            else:
                self.building.color = color.rgba(self.building.color[0], self.building.color[1], self.building.color[2], 1)
        
        def Cancel():
            self.building.buildingMenu.disable()

        def BackMain():
            self.job_menu.disable()
            self.building_menu.enable()

        def Job():
            self.building_menu.disable()
            self.job_menu.enable()
            background = Entity(model='cube', scale=(1, 1, 0.1), parent=self.job_menu, color=color.gray)

            self.jobsDropDown_Menu = DropdownMenu('Jobs', buttons=(
                DropdownMenuButton('Arts'),
                DropdownMenuButton('Business'),
                DropdownMenuButton('Communications'),
                DropdownMenuButton('Education'),
                DropdownMenuButton('Health care'),
                DropdownMenuButton('Hospitality'),
                DropdownMenuButton('Information technology'),
                DropdownMenuButton('Law enforcement'),
                DropdownMenuButton('Sales and Marketing'),
                DropdownMenuButton('Science'),
                DropdownMenuButton('Transportation'),
                DropdownMenuButton('None'),
            ), parent=self.job_menu, position = (-0.4,0.4,0))

            def on_job_click(button):
                self.selected_job = button.text  # Set the selected job when a button is clicked
                addText()

            self.jobsDropDown_Menu.on_click = on_job_click

            back_button = Button(text='Back', color=color.orange, scale_y=0.1, scale_x=0.3, y=-0.35, parent=background)
            back_button.on_click = Func(BackMain)

        buttons = [
            Button(text='Remove', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.building_menu),
            Button(text='Hide', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.building_menu),
            Button(text='Job', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.building_menu),
            Button(text='Cancel', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.building_menu)
        ]
        
        buttons[0].on_click = Func(Remove)
        buttons[1].on_click = Func(Hide)
        buttons[2].on_click = Func(Job)
        buttons[3].on_click = Func(Cancel)

        num_buttons = len(buttons)
        total_height = 0.1 * num_buttons + 0.05 * (num_buttons - 1)
        start_y = total_height / 2 - 0.1 / 2

        for i, button in enumerate(buttons):
            button.y = start_y - i * (0.1 + 0.05)

# building
class Building(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__()
        self.parent=scene
        self.position=position
        self.scale=1
        self.model='cube'
        self.texture='white_cube'
        self.color=color.red
        self.shader=lit_with_shadows_shader
        self.buildingMenu = BuildingMenu(self)
        self.buildingMenu.disable()
        self.jobName = None
        
    def holdInfo(self, jobName):
        if self.jobName != jobName:
            self.employment = round(random.uniform(1, 100))
            self.generalCost = round(random.uniform(1000, 10000), 2)
            self.monthlyCost = round(random.uniform(1000, 9000), 2)
            self.yearCost = self.monthlyCost * 12
            self.water = round(random.uniform(4140, 5580)) * self.employment
            self.food = round(random.uniform(118, 1070)) * self.employment
        
        self.fields = {
            f'General Cost: ${self.generalCost}': (0.4, 0.2),
            f'Cost per Month: ${self.monthlyCost}': (0.4, 0.1),
            f'Cost per Year: ${self.yearCost}': (0.4, 0.0),
            f'Water Consumption: {self.water} ml': (0.4, -0.1),
            f'Food Consumption: {self.food} lbs': (0.4, -0.2),
            f'Employment: {self.employment}': (0.4, -0.3)
        }

        self.jobName = jobName

    def input(self, key):
        if key == 'right mouse down' and mouse.hovered_entity:
            self.buildingMenu.enable()

# menu
class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        self.main_menu = Entity(parent=self, enabled=True)
        self.settings_menu = Entity(parent=self, enabled=False)  # Initially disabled
        mouse.locked = False

        def Play():
            mouse.locked = False
            self.main_menu.disable()

        def BackMain():
            self.settings_menu.disable()
            self.main_menu.enable()

        def Settings():
            self.main_menu.disable()
            self.settings_menu.enable()

            background = Entity(model='cube', scale=(1, 1, 0.1), parent=self.settings_menu, color=color.gray)

            Text('Music Volume', parent=background, y=0.05, x=-0.23, origin=(-0.5, 0))
            music_slider = Slider(0, 100, default=100, height=Text.size * 3, y=0, x=-0.23, step=1, vertical=False, parent=background)
            
            Text('SFX Volume', parent=background, y=-0.05, x=-0.23, origin=(-0.5, 0))
            SFX_slider = Slider(0, 100, default=100, height=Text.size * 3, y=-0.1, x=-0.23, step=1, vertical=False, parent=background)
            
            Text('Frame Rate', parent=background, y=-0.15, x=-0.23, origin=(-0.5, 0))
            frame_slider = Slider(0, 64, default=64, height=Text.size * 3, y=-0.2, x=-0.23, step=1, vertical=False, parent=background)

            back_button = Button(text='Back', color=color.orange, scale_y=0.1, scale_x=0.3, y=-0.35, parent=background)
            back_button.on_click = Func(BackMain)
            
        buttons = [
            Button(text='Play', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.main_menu),
            Button(text='Settings', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.main_menu),
            Button(text='Quit', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.main_menu),
        ]

        buttons[0].on_click = Func(Play)
        buttons[1].on_click = Func(Settings)
        buttons[2].on_click = application.quit
        
        num_buttons = len(buttons)
        total_height = 0.1 * num_buttons + 0.05 * (num_buttons - 1)
        start_y = total_height / 2 - 0.1 / 2

        for i, button in enumerate(buttons):
            button.y = start_y - i * (0.1 + 0.05)
