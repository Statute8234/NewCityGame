import ursina
from ursina import *
from perlin_noise import PerlinNoise
from numpy import floor
from ursina import Default, camera
from ursina.shaders import lit_with_shadows_shader
import time, random, sys
shader_name = lit_with_shadows_shader
# hand made files
import pauseMenu
current_time = time.time()
random.seed(current_time)
ursina.SmoothFollow = True

# camera position
startMenu_camPosition = Vec3(0, 17, -90)
defaultPosition = Vec3(0, 10, 0)
# update
def update_day_night_cycle():
    global time_of_day
    time_of_day += 0.1
    if time_of_day > day_duration:
        time_of_day = 0  # reset to the start of the day

    # Calculate the light intensity and color based on the time of day
    day_fraction = time_of_day / day_duration
    if day_fraction < 0.5:
        # Daytime
        light_intensity = lerp(0.2, 1.0, day_fraction * 2)
        sun.color = lerp(color.gray, color.white, day_fraction * 2)
        sky.color = lerp(color.dark_gray, color.light_gray, day_fraction * 2)
    else:
        # Nighttime
        light_intensity = lerp(1.0, 0.2, (day_fraction - 0.5) * 2)
        sun.color = lerp(color.white, color.gray, (day_fraction - 0.5) * 2)
        sky.color = lerp(color.light_gray, color.dark_gray, (day_fraction - 0.5) * 2)
    
    sun.intensity = light_intensity

def update_season():
    global current_season_idex, current_season
    if time.time() % season_duration < time.dt:
        current_season_idex = (current_season_idex + 1) % len(seasons)
        current_season = seasons[current_season_idex]
        update_terrain_texture()

def update_terrain_texture():
    for entity in scene.entities:
        if isinstance(entity, Ground):
            if current_season == 'spring':
                entity.color = color.lime
            if current_season == 'summer':
                entity.color = color.green
            if current_season == 'autumn':
                entity.color = color.orange
            if current_season == 'winter':
                entity.color = color.black

def update():
    if main_menu.main_menu.enabled:
        camera.position = startMenu_camPosition
    else:
        if camera.position == startMenu_camPosition:
            camera.position = defaultPosition
    update_day_night_cycle()
    update_season()

# ground
class Ground(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'cube'
        self.texture = "grass"
        self.shader = shader_name
noise = PerlinNoise(octaves=random.randint(1, 6), seed=random.randint(0, sys.maxsize))
freq = random.uniform(5, 30)
amp = random.uniform(1, 15)
terrain_radius = 30
center_x = 0
center_z = 0

# circle
def is_within_circle(x, z, radius):
        return sqrt((x - center_x) ** 2 + (z - center_z) ** 2) <= radius

# fill empty spaces
def fill_empty_spaces():
    for x in range(-terrain_radius, terrain_radius):
        for z in range(-terrain_radius, terrain_radius):
            position = Vec3(x, 0, z)
            if is_within_circle(position[0], position[2], terrain_radius):
                if not any([entity.position == position for entity in scene.entities if isinstance(entity, Ground)]):
                    ground = Ground(position=position)
                    ground.y = floor(noise([ground.x / freq, ground.z / freq]) * amp)

# test cubes
class Buildings(Entity):
    def __init__(self, position = (0,0,0)):
        super().__init__()
        self.parent = scene
        self.position = position
        self.scale = 1
        self.model = 'cube'
        self.texture = "white_cube"
        self.shader = shader_name
        self.color = color.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))

# island
avalliblePlaces = []
def Island(position):
    # Create the terrain
    for x in range(-terrain_radius, terrain_radius):
        for z in range(-terrain_radius, terrain_radius):
            if is_within_circle(position[0] + x, position[2] + z, terrain_radius):
                ground = Ground(position=(position[0] + x, 0, position[2] +  z))
                ground.y = position[1] + floor(noise([ground.x / freq, ground.z / freq]) * amp)
                avalliblePlaces.append(ground.position)

# place buildings
def PlaceBuildings(position):
    for space in avalliblePlaces:
        if (space[0], space[1], space[2]) == position:
            building = Buildings(position=(space[0],space[1] + 1, space[2]))
            print("place building")

# dya night cycle
day_duration = 60
time_of_day = 30
# seasons
seasons = ['spring', 'summer', 'autumn', 'winter']
season_duration = 180
current_season_idex = random.randint(0, len(seasons) - 1)
current_season = seasons[current_season_idex]

# game
app = Ursina()
window.fullscreen = False
window.fps_counter.enabled = False
window.cog_button.enabled = False
window.show_ursina_splash = True
window.icon = r'assets\city.png'

main_menu = pauseMenu.MainMenu()
Island(position=(0,0,0))
PlaceBuildings(position=(0,0,0))
#fill_empty_spaces()

sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))
scene.fog_density = (1, 50)
sky = Sky(color=color.light_gray, texture = 'sky_default')
camera = EditorCamera()


if __name__ == "__main__":
    app.run()