#!/bin/bash

cd ./generic-sqed-module-demo/Generators/

python constraint_generator.py
python decoder_generator.py
python modify_generator.py
python qed_generator.py

cd ..

cd ..
