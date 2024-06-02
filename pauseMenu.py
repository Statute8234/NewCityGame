from ursina import *

class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent = camera.ui)

        self.main_menu = Entity(parent = self, enabled = True)
        self.settings_menu = Entity(parent = self, enabled = True)
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

            background = Entity(model = 'cube', scale = 1, parent = self.settings_menu, color = color.gray)
            music_slider = Slider(0, 100, default=100, height=Text.size*3, y=0, x=-0.23, step=1, vertical=False,  parent = background)
            SFX_slider = Slider(0, 100, default=100, height=Text.size*3, y=-0.1, x=-0.23, step=1, vertical=False,  parent = background)
            frame_slider = Slider(0, 64, default=64, height=Text.size*3, y=-0.2, x=-0.23, step=1, vertical=False,  parent = background)
        
        buttons = [
            Button(text='Play', color = color.orange, scale_y = 0.1, scale_x = 0.3, parent = self.main_menu),
            Button(text='Settings', color = color.orange, scale_y = 0.1, scale_x = 0.3, parent = self.main_menu),
            Button(text='Quit', color = color.orange, scale_y = 0.1, scale_x = 0.3, parent = self.main_menu),
        ]

        buttons[0].on_click = Func(Play)
        buttons[1].on_click = Func(Settings)
        buttons[2].on_click = application.quit
        
        num_buttons = len(buttons)
        total_height = 0.1 * num_buttons + 0.05 * (num_buttons - 1)
        start_y = total_height / 2 - 0.1 / 2

        for i, button in enumerate(buttons):
            button.y = start_y - i * (0.1 + 0.05)