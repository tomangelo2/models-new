Instrukcja:

Dla każdego systemu są osobne narzędzia, także skrypty (różnice w kodowaniu znaków).
Jak używać każdego z narzędzi:
Każde obsługiwane jest z wiersza poleceń (terminal w Linux, cmd lub msys w Windows).
[*]convert_model (dla obu systemów identycznie)
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
obj2txt_lin i obj2txt_lin2 różnią się tym, że lin2 obsługuje state i nie ma hardkodowanych wartości oświetlenia (chociaż wkrótce będzie to zmienione, zaciemnia to modele).

konwertuj.sh służy wyłącznie do zautomatyzowania 2 poprzednich skryptów.
Użycie:
"
	./konwertuj.sh <nazwa_pliku_bez_rozszerzenia>
"
konwertuj2.sh robi to samo, lecz zamiast obj2txt_lin wykorzystuje obj2txt_lin2

Z konwertuj_win.sh można korzystać wyłącznie poprzez konsolę msys
That's all, folks :P