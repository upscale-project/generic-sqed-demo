#!/bin/bash

# Pinning yosys version
YOSYS_VERSION=859e52af59e75689f7b0615899bc3356ba5a7ca1

git clone https://github.com/YosysHQ/yosys.git
cd yosys
git checkout -f $YOSYS_VERSION
make -j4
cd ../

