import ursina
from ursina import *
from ursina.prefabs.health_bar import HealthBar
from ursina.shaders import lit_with_shadows_shader
from perlin_noise import PerlinNoise
from numpy import floor
import time, random, sys

current_time = time.time()
random.seed(current_time)

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
        self.health_bar = HealthBar(bar_color=color.red.tint(-.25), roundness=.5, max_value=100, value=100, parent = self, position = (-radius/2,radius + 1,0), scale=(radius,radius / 10,0), show_text=False, show_lines=False)

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

# build Island
noise, freq, amp, terrain_radius, center_x, center_z = 0, 0, 0, 0, 0, 0
def build_basic():
    global noise, freq, amp, terrain_radius, center_x
    noise = PerlinNoise(octaves=random.randint(1, 6), seed=random.randint(0, sys.maxsize))
    freq = random.uniform(5, 30)
    amp = random.uniform(1, 15)
    terrain_radius = 30
    center_x = 0
    center_z = 0

def is_within_circle(x, z, radius):
    return sqrt((x - center_x) ** 2 + (z - center_z) ** 2) <= radius

# island
availible_spots = []
def build_island(position, current_season):
    build_basic()
    dome = Dome(subdivisions=terrain_radius)
    for x in range(-terrain_radius, terrain_radius):
        for z in range(-terrain_radius, terrain_radius):
            if is_within_circle(position[0] + x, position[2] + z, terrain_radius):
                ground = Ground(position=(position[0] + x, 0, position[2] + z))
                ground.y = position[1] + floor(noise([ground.x / freq, ground.z / freq]) * amp)
                ground.change(current_season)
                availible_spots.append(ground.position)
