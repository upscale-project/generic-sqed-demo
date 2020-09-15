#!/bin/bash

# generate the btor
echo "Generating BTOR2 using yosys"
./yosys/yosys -q -s gen-btor.ys

# run pono
echo ""
echo "Running pono"
./pono/build/pono -v 1 -k 12 ./ridecore.btor2
