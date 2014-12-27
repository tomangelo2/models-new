#-*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

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
        self.texture2 = ''
        self.ambient = [0.0, 0.0, 0.0]
        self.diffuse = [0.8, 0.8, 0.8]
        self.specular = [0.5, 0.5, 0.5]
        self.state = 0
        self.version = 2
        self.lod = 0

class ModelFormat:
    def read(self, filename, model, params):
        raise ModelFormatException('Reading not implemented')
    
    def write(self, filename, model, params):
        raise ModelFormatException('Writing not implemented')

class ModelFormatException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return 'Model format error: {}'.format(message)

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
