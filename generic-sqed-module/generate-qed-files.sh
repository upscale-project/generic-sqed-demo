#!/bin/bash

cd Generators

python constraint_generator.py
python decoder_generator.py
python modify_generator.py
python qed_generator.py

cd ..

