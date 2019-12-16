#!/bin/bash

cd ./SQED-Generator/Generators/

python constraint_generator.py
python decoder_generator.py
python modify_generator.py
python qed_generator.py

cd ..

cd ..
