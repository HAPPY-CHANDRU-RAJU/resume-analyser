#!/bin/bash

python3.9 preprocessing.py

cd data

for f in *.pdf
do
  pdftotext -enc UTF-8 $f
done

mv -v *.txt ../txt-data/

cd ../

python3.9 main.py
