(This metod is obsolete, are you sure you don't want to use Colobot-Model-Converter?)

Instructions:

For every OS there are separated tools, even scripts (because of 'end of line' chars).

How to use them:

Every tool is controled by cmd/terminal. For every OS they are working the same way. You only need to add suffix .exe if you are running them under Windows.

convert_model
	"Usage:

	 Convert files:
	   ./convert_model -i input_file -if input_format -o output_file -of output_format

	 Dump info:
	   ./convert_model -d -i input_file -if input_format

	 Help:
	   ./convert_model -h

	Model formats:
	 old       => old binary format [mod]
	 new_bin   => new binary format 
	 new_txt   => new text format [txt]
"
obj2txt_<sys>.py
You need Python3, this won't work under Python2.
	"# Wavefront .OBJ -> Colobot text model format converter
	# Usage:
	#   obj2txt.py input.obj output.txt 1
	#
	#       input.obj       input file
	#       output.txt      output file
	#       1               output version (1 - with LOD, 2 - without LOD)
"

konwertuj.sh is just an script that run 2 previous programs.
Usage:
"
	./konwertuj.sh <name_of_file_without_extension>
"