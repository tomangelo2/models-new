#-*- coding: utf-8 -*-
# Implements Colobot model format writing
# Copyright (c) 2014 Tomasz Kapuściński

import geometry

class ColobotFormat(geometry.ModelFormat):
    def read(self, filename, model, params):
        file = open(filename, 'r')
        
        triangle = geometry.Triangle()
        
        while True:
            line = file.readline()
            
            # eof
            if len(line) == 0:
                break
            
            # comments are ignored
            if line[0] == '#':
                continue
            
            # remove eol
            if line[len(line)-1] == '\n':
                line = line[:len(line)-1]
        
            values = line.split(' ');
            cmd = values[0]
            
            if cmd == 'version':
                model.version = int(values[1])
            elif cmd == 'triangles':
                continue
            elif cmd == 'p1':
                triangle.vertices[0] = parse_vertex(values)
            elif cmd == 'p2':
                triangle.vertices[1] = parse_vertex(values)
            elif cmd == 'p3':
                triangle.vertices[2] = parse_vertex(values)
            elif cmd == 'mat':
                parse_material(triangle.material, values)
            elif cmd == 'tex1':
                triangle.material.texture = values[1]
            elif cmd == 'tex2':
                triangle.material.texture2 = values[1]
            elif cmd == 'var_tex2':
                continue
            elif cmd == 'lod_level':
                triangle.material.lod = int(values[1])
            elif cmd == 'state':
                triangle.material.state = int(values[1])
                model.triangles.append(triangle)
                triangle = geometry.Triangle()
        
        file.close()
    
    def write(self, filename, model, params):
        file = open(filename, 'w')
        
        version = 2
        
        if 'version' in params:
            version = int(params['version'])

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
            file.write('tex1 {}\n'.format(material.texture))
            file.write('tex2 {}\n'.format(material.texture2))
            file.write('var_tex2 Y\n')

            if version == 1:
                file.write('lod_level 0\n')

            file.write('state ' + str(material.state) + '\n')
            file.write('\n')

        file.close()


def register(formats):
    formats['colobot'] = ColobotFormat()

def parse_vertex(values):
    vertex_coord = geometry.VertexCoord(float(values[2]), float(values[3]), float(values[4]))
    normal = geometry.Normal(float(values[6]), float(values[7]), float(values[8]))
    tex_coord = geometry.TexCoord(float(values[10]), float(values[11]))
    
    return geometry.Vertex(vertex_coord, tex_coord, normal)

def parse_material(material, values):
    for i in range(3):
        material.diffuse[i] = float(values[2+i])
        material.ambient[i] = float(values[7+i])
        material.specular[i] = float(values[12+i])