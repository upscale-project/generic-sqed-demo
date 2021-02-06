#!/bin/bash

cd ./sqed-generator/SQED-Generator/Generators/

python ./generate_sqed.py ../FormatFiles/RV32M-ridecore_format.txt ../QEDFiles

cp ../Design_Independent_QED_Files/* ../QEDFiles

cd ..

cd ..

cd ..
