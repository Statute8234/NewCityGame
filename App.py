import ursina
from ursina import *
from numpy import floor
import time, random, sys
from ursina.texture import Texture
from perlin_noise import PerlinNoise
from ursina.shaders import lit_with_shadows_shader
# hand made
import GameObjects

current_time = time.time()
random.seed(current_time)
ursina.SmoothFollow = True

# camera
startMenu_camPosition = Vec3(0, 17, -90)
defaultPosition = Vec3(0,10,0)

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

# update season
def update_season():
    global current_season_idex, current_season
    if time.time() % season_duration < time.dt:
        current_season_idex = (current_season_idex + 1) % len(seasons)
        current_season = seasons[current_season_idex]
        update_terrain_texture()

def update_terrain_texture():
    for entity in scene.entities:
        if isinstance(entity, GameObjects.Ground):
            if current_season == 'spring':
                entity.color = color.lime
            if current_season == 'summer':
                entity.color = color.green
            if current_season == 'autumn':
                entity.color = color.orange
            if current_season == 'winter':
                entity.color = color.yellow

# Update weather
def update_weather():
    global weather_timer, current_weather_index, current_weather, weather_duration
    weather_timer += 1
    if weather_timer > weather_duration:
        weather_timer = 0
        current_weather_index = (current_weather_index + 1) % len(weather_types)
        current_weather = weather_types[current_weather_index]
        apply_weather_effects(current_weather)
    elif weather_timer == 0:
        weather_duration = random.randint(120,999)

def apply_weather_effects(weather):
    if weather == 'clear':
        sky.color = color.light_gray
        scene.fog_density = (1, 50)
        disable_rain()
        disable_snow()
    elif weather == 'rain':
        sky.color = color.gray
        scene.fog_density = (10, 50)
        enable_rain()
        disable_snow()
    elif weather == 'snow':
        sky.color = color.white
        scene.fog_density = (5, 50)
        enable_snow()
        disable_rain()
# Enable/disable rain
rain_entities = []

def enable_rain():
    global rain_entities
    if not rain_entities:
        for i in range(1000):
            raindrop = Entity(model='cube', scale=(0.1, 1, 0.1), color=color.blue, position=(random.uniform(-100, 100), 100, random.uniform(-100, 100)))
            raindrop.animate_y(-10, duration=random.uniform(0,2), curve=curve.linear, loop=True)
            rain_entities.append(raindrop)

def disable_rain():
    global rain_entities
    for raindrop in rain_entities:
        destroy(raindrop)
    rain_entities = []

# Enable/disable snow
snow_entities = []

def enable_snow():
    global snow_entities
    if not snow_entities:
        for i in range(1000):
            snowflake = Entity(model='cube', scale=(0.1, 0.1, 0.1), color=color.white, position=(random.uniform(-100, 100), 100, random.uniform(-100, 100)))
            snowflake.animate_y(-10, duration=random.uniform(0,2), curve=curve.linear, loop=True)
            snow_entities.append(snowflake)

def disable_snow():
    global snow_entities
    for snowflake in snow_entities:
        destroy(snowflake)
    snow_entities = []

def update():
    if main_menu.main_menu.enabled:
        camera.position = startMenu_camPosition
    else:
        if camera.position == startMenu_camPosition:
            camera.position = defaultPosition
    update_day_night_cycle()
    update_weather()
    update_season()

# dya night cycle
day_duration = 60
time_of_day = 30
# weather
weather_types = ['clear', 'rain', 'snow']
weather_duration = random.randint(1,999)
current_weather_index = random.randint(0, len(weather_types) - 1)
current_weather = weather_types[current_weather_index]
weather_timer = 0
# seasons
seasons = ['spring', 'summer', 'autumn', 'winter']
season_duration = 180
current_season_idex = random.randint(0, len(seasons) - 1)
current_season = seasons[current_season_idex]

"""Create Island"""
noise = PerlinNoise(octaves=random.randint(1,6), seed=random.randint(0, sys.maxsize))
freq = random.uniform(5, 30)
amp = random.uniform(1, 15)
terrain_radius = 30
center_x = 0
center_z = 0

def is_within_circle(x, z, radius):
    return sqrt((x - center_x) ** 2 + (z - center_z) ** 2) <= radius

# island
def Island(position):
    for x in range(-terrain_radius,terrain_radius):
        for z in range(-terrain_radius,terrain_radius):
            if is_within_circle(position[0] + x, position[2] + z, terrain_radius):
                ground = GameObjects.Ground(position=(position[0] + x, 0, position[2] + z))
                ground.y = position[1] + floor(noise([ground.x / freq, ground.z / freq]) * amp)

# game
app = Ursina()
window.fullscreen = False
window.fps_counter.enabled = False
window.cog_button.enabled = False
window.show_ursina_splash = True
window.icon = r'assets\city.png'
main_menu = GameObjects.MainMenu()
# Island
Island(position=(0,0,0))
# camera
camera = EditorCamera()
sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))
scene.fog_density = (1, 50)
sky = Sky(color=color.light_gray, texture= 'sky_default', rotation_z = 90)

if __name__ == "__main__":
    app.run()
