import ursina
from ursina import *
from ursina.shaders import lit_with_shadows_shader

# on camera UI
class CameraMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.settings_menu = Entity(parent=self, enabled=False)  # Initially disabled

        def Hide():
            self.main_menu.disable()

        def BackMain():
            self.settings_menu.disable()
            self.main_menu.enable()

        def Settings():
            self.main_menu.disable()
            self.settings_menu.enable()

            background = Entity(model='quad', scale=(1, 1), parent=self.settings_menu, color=color.gray)

            Text('Music Volume', parent=background, y=0.05, x=-0.23, origin=(-0.5, 0))
            music_slider = Slider(0, 100, default=100, height=Text.size * 3, y=0, x=-0.23, step=1, vertical=False, parent=background)
            
            Text('SFX Volume', parent=background, y=-0.05, x=-0.23, origin=(-0.5, 0))
            SFX_slider = Slider(0, 100, default=100, height=Text.size * 3, y=-0.1, x=-0.23, step=1, vertical=False, parent=background)
            
            Text('Frame Rate', parent=background, y=-0.15, x=-0.23, origin=(-0.5, 0))
            frame_slider = Slider(0, 64, default=64, height=Text.size * 3, y=-0.2, x=-0.23, step=1, vertical=False, parent=background)

            back_button = Button(text='Back', color=color.orange, scale_y=0.1, scale_x=0.3, y=-0.35, parent=background)
            back_button.on_click = Func(BackMain)
        
        def Home():
            print("Home")

        background = Entity(model='quad', scale=(1, 0.2), parent=self.main_menu, color=color.gray, y=-0.5)
        hideButton = Button(scale_y=0.09, scale_x=0.09, parent=self.main_menu, texture=r'Assets\Menu_Images\logout.png', y=-0.45, x=0.45)
        hideButton.on_click = Func(Hide)
        settingsButton = Button(scale_y=0.09, scale_x=0.09, parent=self.main_menu, texture=r'Assets\Menu_Images\gear.png', y=-0.45, x=0.35)
        settingsButton.on_click = Func(Settings)
        homeButton = Button(scale_y=0.09, scale_x=0.09, parent=self.main_menu, texture=r'Assets\Menu_Images\home-icon-silhouette.png', y=-0.45, x=0.25)
        homeButton.on_click = Func(Home)

        TextField(bg=color.dark_gray, text="City Name", parent=self.main_menu, scale=(0.002, 0.02), y=-0.45, x=-0.45, z=-1)
# menu
class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.settings_menu = Entity(parent=self, enabled=False)  # Initially disabled

        def Play():
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

# building menu
class CapitalMenu(Entity):
    def __init__(self, capital):
        super().__init__(parent=camera.ui)
        self.capital = capital
        self.menu = Entity(parent=self, enabled=False)
        
        def upgrade():
            print("Upgrade clicked")
        
        def buy_new_island():
            print("Buy new Island clicked")
        
        def build_new_building():
            print("Build new building")
        
        def military():
            print("Military clicked")
        
        def Cancel():
            self.menu.disable()

        buttons = [
            Button(text='Upgrade', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.menu),
            Button(text='Buy new Island', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.menu),
            Button(text='Build new building', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.menu),
            Button(text='Military', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.menu),
            Button(text='Cancel', color=color.orange, scale_y=0.1, scale_x=0.3, parent=self.menu)
        ]

        buttons[0].on_click = Func(upgrade)
        buttons[1].on_click = Func(buy_new_island)
        buttons[2].on_click = Func(build_new_building)
        buttons[3].on_click = Func(military)
        buttons[4].on_click = Func(Cancel)

        num_buttons = len(buttons)
        total_height = 0.1 * num_buttons + 0.05 * (num_buttons - 1)
        start_y = total_height / 2 - 0.1 / 2

        for i, button in enumerate(buttons):
            button.y = start_y - i * (0.1 + 0.05)
