# Wavefront .OBJ -> Colobot text model format converter
# Usage:
#   obj2txt.py input.obj output.txt 1
#
#       input.obj       input file
#       output.txt      output file
#       1               output version (1 - with LOD, 2 - without LOD)

import re
import sys

class VertexCoord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class TexCoord:
    def __init__(self, u, v):
        self.u = u
        self.v = v

class Normal:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Vertex:
    def __init__(self, vertex, tex, normal):
        self.x = vertex.x
        self.y = vertex.y
        self.z = vertex.z
        self.u = tex.u
        self.v = tex.v
        self.nx = normal.x
        self.ny = normal.y
        self.nz = normal.z

class Triangle:
    def __init__(self):
        self.vertices = [0, 0, 0]
        self.material = Material()

class Model:
    def __init__(self):
        self.triangles = []

class Material:
    def __init__(self):
        self.texture = 'unknown'
        self.ambient = [0.0, 0.0, 0.0]
        self.diffuse = [0.8, 0.8, 0.8]
        self.specular = [0.5, 0.5, 0.5]
        self.state = '0'


# triangulates polygon
def triangulate(vertices):
    result = []

    first = vertices[0]
    third = vertices[1]

    count = len(vertices)

    for i in range(2, count):
        second = third
        third = vertices[i]

        triangle = Triangle()

        # reverses order
        triangle.vertices[0] = first
        triangle.vertices[2] = second
        triangle.vertices[1] = third
        
        result.append(triangle)

    return result


# reads Wavefront .MTL material file
def read_mtl_file(filename):
    materials = {}
    
    file = open(filename, 'r')

    pattern = re.compile(r'^.+(\[(\d+)\])$')

    while True:
        line = file.readline()

        if len(line) == 0:
            break

        if line[len(line)-1] == '\n':
            line = line[:len(line)-1]
        
        parts = line.split(' ')

        if parts[0] == 'newmtl':
            current_material = Material()
            materials[parts[1]] = current_material

            match = pattern.match(parts[1])

            if match is not None:
                current_material.state = match.group(2)
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


# reads model in Wavefront .OBJ file
def read_obj_model(filename):

    # lists with parsed vertex attributes
    vertex_coords = []
    tex_coords = []
    normals = []
    materials = {}

    # list for resulting triangles
    model = Model()

    # read file
    file = open(sys.argv[1], 'r')

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
            vertex_coords.append(VertexCoord(float(parts[1]), float(parts[2]), -float(parts[3])))
        elif parts[0] == 'vt':
            tex_coords.append(TexCoord(float(parts[1]), 1 - float(parts[2])))
        elif parts[0] == 'vn':
            normals.append(Normal(float(parts[1]), float(parts[2]), -float(parts[3])))
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

                polygon.append(Vertex(vert_coord, tex_coord, normal))

            # triangulate polygon
            new_triangles = triangulate(polygon)

            # save vertices
            for triangle in new_triangles:
                triangle.material = current_material
                model.triangles.append(triangle)
    
    file.close()

    return model


# writes model in new Colobot text format
def write_colobot_model(filename, model, version):
    file = open(filename, 'w')

    # write header
    file.write('# Colobot text model\n')
    file.write('\n')
    file.write('### HEAD\n')
    file.write('version ' + str(version) + '\n')
    file.write('total_triangles ' + str(len(model.triangles)) + '\n')
    file.write('\n')
    file.write('### TRIANGLES\n')

    # write triangles
    for triangle in model.triangles:
        # write vertices
        for i in range(3):
            vertex = triangle.vertices[i]
            file.write('p{0} c {1} {2} {3}'.format(i+1, vertex.x, vertex.y, vertex.z))
            file.write(' n {0} {1} {2}'.format(vertex.nz, vertex.ny, vertex.nz))
            file.write(' t1 {0} {1}'.format(vertex.u, vertex.v))
            file.write(' t2 {0} {1}\n'.format(vertex.u, vertex.v))

        material = triangle.material
        
        file.write('mat dif {0} {1} {2} 0'.format(material.diffuse[0], material.diffuse[1], material.diffuse[2]))
        file.write(' amb {0} {1} {2} 0'.format(material.ambient[0], material.ambient[1], material.ambient[2]))
        file.write(' spc {0} {1} {2} 0\n'.format(material.specular[0], material.specular[1], material.specular[2]))
        file.write('tex1 ' + material.texture + '\n')
        file.write('tex2 \n')
        file.write('var_tex2 Y\n')

        if version == 1:
            file.write('lod_level 0\n')

        file.write('state ' + material.state + '\n')
        file.write('\n')

    file.close()


version = 1

if len(sys.argv) > 3:
    version = int(sys.argv[3])

model = read_obj_model(sys.argv[1])
write_colobot_model(sys.argv[2], model, version)
