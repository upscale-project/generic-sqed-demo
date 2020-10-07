#!/bin/bash

git clone https://github.com/upscale-project/pono.git
cd pono
./contrib/setup-btor2tools.sh
./contrib/setup-bison.sh
./contrib/setup-smt-switch.sh
./configure.sh
cd build
make -j4
make test
cd ../../
