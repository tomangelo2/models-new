#!/bin/sh

echo "$1";
python3 obj2txt_lin.py "$(basename "$1").obj" "$(basename "$1").txt" 2;
./convert_model -i "$(basename "$1").txt" -if new_txt -o "$(basename "$1").mod" -of old;
echo "Done";