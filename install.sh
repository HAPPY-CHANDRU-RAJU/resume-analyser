#!/bin/bash
python3.9 uploader.py

python3.9 preprocessing.py

cd data

for f in *.pdf
do
  pdftotext -enc UTF-8 $f
done

echo "Converting...."


mv *.txt ../txt-data/
cd ../

touch result.json

python3.9 main.py

python3.9 finalplot.py
