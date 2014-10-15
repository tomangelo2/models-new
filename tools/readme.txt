Instrukcja:

Dla każdego systemu są osobne narzędzia, także skrypty (różnice w kodowaniu znaków).

Jak używać każdego z narzędzi:

Każde obsługiwane jest z wiersza poleceń (terminal w Linux, cmd lub msys w Windows).

convert_model (dla obu systemów niemal identycznie, jednak w przypadku systemów Windows zamiast ./convert_model piszemy convert_model.exe)
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
Wymagany jest Python 3, skrypt nie działa na Python 2.
	"# Wavefront .OBJ -> Colobot text model format converter
	# Usage:
	#   obj2txt.py input.obj output.txt 1
	#
	#       input.obj       input file
	#       output.txt      output file
	#       1               output version (1 - with LOD, 2 - without LOD)
"

konwertuj.sh służy wyłącznie do zautomatyzowania 2 poprzednich skryptów.
Użycie:
"
	./konwertuj.sh <nazwa_pliku_bez_rozszerzenia>
"

Skrypt konwertuj_win.sh wykorzystuje funkcje powłoki bash, więc do działania wymaga konsoli msys (nie twierdzę, że tylko w msys, być może cygwin czy inne tego typu programy także będą działać, jednak nie testowałem na nich tego skryptu).