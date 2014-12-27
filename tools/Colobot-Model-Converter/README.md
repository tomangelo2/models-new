Colobot-Model-Converter
=======================

This program can be used to convert various 3D model formats to and from model formats used by Colobot.

For now only conversion from Wavefront .OBJ format to Colobot new text format (version 1 and 2) is supported.


Basic usage
-----------

To convert one format to another you need to run this program in terminal.

```
converter.py [switches]
```

For example, to convert .obj file to Colobot format, use can use following command:

```
converter.py -i box.obj -if obj -o box.txt -of colobot
```

By default Colobot format version 2 is used for output. If you need version 1, you need to add output parameter like this:

```
converter.py -i box.obj -if obj -o box.txt -of colobot -op version=1
```


Command line switches
---------------------

Switch             | Description
-------------------|----------------------------------------
-i *filename*      | Sets input file name to *filename*
-if *format*       | Sets input format to *format*
-ip *key*=*value*  | Adds input format parameter *key* with value *value*
-o *filename*      | Sets output file name to *filename*
-of *format*       | Sets output format to *format*
-op *key*=*value*  | Adds output format parameter *key* with value *value*


Supported formats
-----------------

Below are listed all formats supported by this converter. A given format can have read only, write only and read/write access. Read only means you can convert this format to something else but not into it. Write only means you can convert other format to this format but can't convert from it. Read/write means you can convert to and from this format.

Format name      | Access     | Description
-----------------|------------|---------------------------
colobot          | read/write | Colobot new text format
obj              | read only  | Wavefront .OBJ format


State specification
-------------------

Colobot meshes specify internal state of each triangle that changes behaviour of rendering engine. You can specify state in material name like this: *Material name [state]*. *state* has to be a list of numbers or state names.

Valid state names are listed in table below. Some states are not properly documented and have unknown effects.

Name                | Code    | Description
--------------------|---------|---------------------------------------
normal              | 0       | Normal texture
ttexture_black      | 1       | Texture with black color transparency
ttexture_white      | 2       | Texture with white color transparency
ttexture_diffuse    | 4       | Texture with transparency
wrap                | 8       | Wrap mode
clamp               | 16      | Clamp mode
light               | 32      | Completely bright
dual_black          | 64      | Dual black ?
dual_white          | 128     | Dual white ?
part1               | 256     | Part 1
part2               | 512     | Part 2
part3               | 1024    | Part 3
part4               | 2048    | Part 4
2face               | 4096    | Render both faces
alpha               | 8192    | Transparency with alpha channel
second              | 16384   | Use second texture
fog                 | 32768   | Render fog
tcolor_black        | 65536   | Black color is transparent
tcolor_white        | 131072  | White color is transparent
text                | 262144  | Used for rendering text
opaque_texture      | 524288  | Opaque texture
opaque_color        | 1048576 | Opaque color


Changelog
---------

- 1.3
  - code refactored
  - added simple and extensible API for format conversion
  - added command line switches
- 1.2
  - code refactored, split into separate files
- 1.1
  - added alternate state specification
  - default output format version changed to 2
- 1.0
  - state specification in material name ("Material [state]")