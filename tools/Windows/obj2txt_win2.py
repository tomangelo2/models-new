# Wavefront .OBJ -> Colobot text model format converter
# Usage:
#   obj2txt.py input.obj output.txt 1
#
#       input.obj       input file
#       output.txt      output file
#       1               output version (1 - with LOD, 2 - without LOD)

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
		
	def __repr__(self):
		return 'c {0} {1} {2} n {3} {4} {5} t1 {6} {7} t2 {6} {7}'.format(self.x, self.y, self.z, self.nx, self.ny, self.nz, self.u, self.v)

class Material:
	def __init__(self):
		self.texture = 'unknown'

def triangulate(vertices):
	result = []
	
	first = vertices[0]
	third = vertices[1]
	
	count = len(vertices)
	
	for i in range(2, count):
		second = third
		third = vertices[i]
		
		triangle = [first, second, third]
		
		result.append(triangle)
	
	return result

def parse_materials(materials, filename):
	file = open(filename, 'r')
	lines = file.readlines()
	file.close()
	
	for line in lines:
		parts = line.split(' ')
		
		if parts[0] == 'newmtl':
			current_material = Material()
			materials[parts[1]] = current_material
		elif parts[0] == 'map_Kd':
			name = parts[1]
			name = name[:len(name)-1]
			current_material.texture = name


# lists with parsed vertex attributes
vertex_coords = []
tex_coords = []
normals = []
materials = {}

# list for resulting triangles
triangles = []

# read file
file = open(sys.argv[1], 'r')
lines = file.readlines()
file.close()

# parse lines
for line in lines:
	parts = line.split(' ')

	if parts[0] == 'mtllib':
		name = parts[1]
		name = name[:len(name)-1]
		parse_materials(materials, name)
	elif parts[0] == 'v':
		vertex_coords.append(VertexCoord(float(parts[1]), float(parts[2]), float(parts[3])))
	elif parts[0] == 'vt':
		tex_coords.append(TexCoord(float(parts[1]), 1 - float(parts[2])))
	elif parts[0] == 'vn':
		normals.append(Normal(float(parts[1]), float(parts[2]), float(parts[3])))
	elif parts[0] == 'usemtl':
		current_texture = materials[parts[1]].texture
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
			triangle.append(current_texture)
			triangles.append(triangle)


# create colobot model file

file = open(sys.argv[2], 'w')

version = int(sys.argv[3])

# write header
file.write('# Colobot text model\n')
file.write('\n')
file.write('### HEAD\n')
file.write('version ' + str(version) + '\n')
file.write('total_triangles ' + str(len(triangles)) + '\n')
file.write('\n')
file.write('### TRIANGLES\n')

# write triangles
for triangle in triangles:
	file.write('p1 ' + str(triangle[0]) + '\n')
	file.write('p2 ' + str(triangle[1]) + '\n')
	file.write('p3 ' + str(triangle[2]) + '\n')
	file.write('mat dif 1 1 1 0 amb 0.5 0.5 0.5 0 spc 0 0 0 0\n')
	file.write('tex1 ' + triangle[3] + '\n')
	file.write('tex2 \n')
	file.write('var_tex2 Y\n')
	
	if version == 1:
		file.write('lod_level 0\n')
	
	file.write('state 0\n')
	file.write('\n')

file.close()
