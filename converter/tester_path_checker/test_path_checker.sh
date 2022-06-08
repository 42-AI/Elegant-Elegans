#!/bin/bash

printf "Path_Checker Tester:\n"

printf "Directory doesn't exist: \n"
cd ../.. && python -m converter --path [test]

cd ../.. && mkdir test
cd ../.. && chmod 000 test
printf "Directory exists but doesn't grant access: \n"
cd ../.. && python -m converter --path [test]

cd ../.. && chmod 755 test
cd ../../test && touch file.txt
printf "Directory exists, has access rights but file other than .json or .tiff exists: \n"
cd ../.. && python -m converter --path [test]

cd ../../test && rm file.txt
cd ../../test && touch file.tiff
printf "Directory exists, has access rights but no .json is found: \n"
cd ../.. && python -m converter --path [test]

cd ../../test && touch file.json
printf "Directory exists, has access rights but less than 100 .tiff files are found: \n"
cd ../.. && python -m converter --path [test]

for i in range(100)
do
    cd ../../test && touch file${i}.tiff
done
printf "Directory exists, has access rights and there are 100 .tiff files: \n"
cd ../.. && python -m converter --path [test]

cd ../.. && rm -rf test