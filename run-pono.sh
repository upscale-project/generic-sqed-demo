#!/bin/bash

# generate the btor
echo "Generating BTOR2 using yosys"
# prefer local version
if [ -f ./yosys/yosys ]; then
    YOSYS=./yosys/yosys
elif [ `which yosys` ]; then
    YOSYS=yosys
else
    echo "Could not find Yosys. Needed to generate BTOR2"
    exit 1
fi

$YOSYS -q -s gen-btor.ys

# run pono
echo ""
echo "Running pono"
# prefer local version
if [ -f ./pono/build/pono ]; then
    PONO=./pono/build/pono
elif [ `which pono` ]; then
    PONO=pono
else
    echo "Could not find Pono."
    exit 1
fi
$PONO -v 1 -k 12 --vcd ridecore-trace.vcd ./ridecore.btor2
