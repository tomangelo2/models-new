#-*- coding: utf-8 -*-
# Colobot Model Converter
# Version 1.2
# Copyright (c) 2014 Tomasz Kapuściński

import sys
import geometry
import objformat
import colobotformat

# register model formats
formats = {}

objformat.register(formats)
colobotformat.register(formats)

# parse arguments
i = 1
n = len(sys.argv)

in_filename = ''
in_format = ''
in_params = {}

out_filename = ''
out_format = ''
out_params = {}

while i < n:
    arg = sys.argv[i]
    value = sys.argv[i+1]
    
    if arg == '-i':
        in_filename = value
        i = i + 2
    elif arg == '-if':
        in_format = value
        i = i + 2
    elif arg == '-ip':
        pair = value.split('=')
        in_params[pair[0]] = pair[1]
        i = i + 2
    elif arg == '-o':
        out_filename = value
        i = i + 2
    elif arg == '-of':
        out_format = value
        i = i + 2
    elif arg == '-op':
        pair = value.split('=')
        out_params[pair[0]] = pair[1]
        i = i + 2
    else:
        raise Exception('Unknown switch: {}'.format(arg))

# convert file
model = geometry.Model()

formats[in_format].read(in_filename, model, in_params)
formats[out_format].write(out_filename, model, out_params)
