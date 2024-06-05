from ursina import *

class Dome(Entity):
    def __init__(self, subdivisions=10, radius=5, **kwargs):
        super().__init__()
        self.model = self.create_dome(subdivisions, radius)
        self.texture = 'white_cube'
        self.scale = radius
        self.collider = 'mesh'

    def create_dome(self, subdivisions, radius):
        verts = []
        tris = []
        for i in range(subdivisions + 1):
            for j in range(subdivisions + 1):
                theta = i / subdivisions * pi
                phi = j / subdivisions * pi * 2
                x = sin(theta) * cos(phi)
                y = cos(theta)
                z = sin(theta) * sin(phi)
                verts.append((x, y, z) * radius)

        for i in range(subdivisions):
            for j in range(subdivisions):
                v1 = i * (subdivisions + 1) + j
                v2 = v1 + (subdivisions + 1)
                v3 = v1 + 1
                v4 = v2 + 1
                if j % 2 == 0:
                    tris.extend([(v1, v2, v3), (v4, v3, v2)])
                else:
                    tris.extend([(v1, v2, v4), (v1, v4, v3)])

        return Mesh(vertices=verts, triangles=tris)

app = Ursina()

dome = Dome(subdivisions=32, radius=5)

app.run()
