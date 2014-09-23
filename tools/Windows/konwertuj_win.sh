#!/bin/sh

echo "$1";
python3 obj2txt_win.py "$(basename "$1").obj" "$(basename "$1").txt" 2;
./convert_model.exe -i "$(basename "$1").txt" -if new_txt -o "$(basename "$1").mod" -of old;
echo "Done";