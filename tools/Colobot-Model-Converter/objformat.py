#-*- coding: utf-8 -*-
# Contains implementation of Wavefront .OBJ importer
# Copyright (c) 2014 Tomasz Kapuściński

import re
import geometry

class ObjFormat(geometry.ModelFormat):
    def read(self, filename, model, params):
        # lists with parsed vertex attributes
        vertex_coords = []
        tex_coords = []
        normals = []
        materials = {}

        # read file
        file = open(filename, 'r')

        # parse lines
        while True:
            line = file.readline()

            if len(line) == 0:
                break

            if line[len(line)-1] == '\n':
                line = line[:len(line)-1]

            parts = line.split(' ')

            if parts[0] == 'mtllib':
                name = parts[1]
                materials = read_mtl_file(name)
            elif parts[0] == 'v':
                vertex_coords.append(geometry.VertexCoord(float(parts[1]), float(parts[2]), -float(parts[3])))
            elif parts[0] == 'vt':
                tex_coords.append(geometry.TexCoord(float(parts[1]), 1 - float(parts[2])))
            elif parts[0] == 'vn':
                normals.append(geometry.Normal(float(parts[1]), float(parts[2]), -float(parts[3])))
            elif parts[0] == 'usemtl':
                current_material = materials[parts[1]]
            elif parts[0] == 'f':
                polygon = []

                # parse vertices
                for i in range(1, len(parts)):
                    elements = parts[i].split('/')

                    vert_coord = vertex_coords[int(elements[0]) - 1]
                    tex_coord = tex_coords[int(elements[1]) - 1]
                    normal = normals[int(elements[2]) - 1]

                    polygon.append(geometry.Vertex(vert_coord, tex_coord, normal))

                # triangulate polygon
                new_triangles = geometry.triangulate(polygon)

                # save vertices
                for triangle in new_triangles:
                    triangle.material = current_material
                    model.triangles.append(triangle)

        file.close()


# register obj format
def register(formats):
    formats['obj'] = ObjFormat()
    

# state regex pattern
state_pattern = re.compile(r'^.+(\[(.+?)\])$')

# state dictionary
state_dictionary = {}

state_dictionary['normal'] = 0                      # normal texture
state_dictionary['ttexture_black'] = 1 << 0         # black texture is transparent
state_dictionary['ttexture_white'] = 1 << 1         # white texture is transparent
state_dictionary['ttexture_diffuse'] = 1 << 2       # transparent texture
state_dictionary['wrap'] = 1 << 3                   # wrap mode
state_dictionary['clamp'] = 1 << 4                  # clamp mode
state_dictionary['light'] = 1 << 5                  # completely bright
state_dictionary['dual_black'] = 1 << 6             # dual black ?
state_dictionary['dual_white'] = 1 << 7             # dual white ?
state_dictionary['part1'] = 1 << 8                  # part 1
state_dictionary['part2'] = 1 << 9                  # part 2
state_dictionary['part3'] = 1 << 10                 # part 3
state_dictionary['part4'] = 1 << 11                 # part 4
state_dictionary['2face'] = 1 << 12                 # render both faces
state_dictionary['alpha'] = 1 << 13                 # alpha channel is transparency
state_dictionary['second'] = 1 << 14                # use second texture
state_dictionary['fog'] = 1 << 15                   # render fog
state_dictionary['tcolor_black'] = 1 << 16          # black color is transparent
state_dictionary['tcolor_white'] = 1 << 17          # white color is transparent
state_dictionary['text'] = 1 << 18                  # used for rendering text
state_dictionary['opaque_texture'] = 1 << 19        # opaque texture
state_dictionary['opaque_color'] = 1 << 20          # opaque color

# parses material state
def parse_state(text):
    state = 0

    for value in text.split(','):
        if value in state_dictionary:
            value = state_dictionary[value]
        state |= int(value)

    return state

# reads Wavefront .MTL material file
def read_mtl_file(filename):
    materials = {}

    file = open(filename, 'r')

    while True:
        line = file.readline()

        if len(line) == 0:
            break

        if line[len(line)-1] == '\n':
            line = line[:len(line)-1]

        parts = line.split(' ')

        if parts[0] == 'newmtl':
            current_material = geometry.Material()

            match = state_pattern.match(parts[1])

            if match is not None:
                current_material.state = parse_state(match.group(2))

            materials[parts[1]] = current_material
        elif parts[0] == 'Ka':
            for i in range(3):
                current_material.ambient[i] = float(parts[i+1])
        elif parts[0] == 'Kd':
            for i in range(3):
                current_material.diffuse[i] = float(parts[i+1])
        elif parts[0] == 'Ks':
            for i in range(3):
                current_material.specular[i] = float(parts[i+1])
        elif parts[0] == 'map_Kd':
            current_material.texture = parts[1]

    file.close()

    return materials
