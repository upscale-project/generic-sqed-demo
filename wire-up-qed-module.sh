#!/bin/bash

cd ./qed-wireup-patches

# Update the topsim module to wire up the QED module

# Add "(* keep *)" pragmas to preserve certain wires for model checking 
patch -i ./step0-topsim-changes.patch ../ridecore-src-buggy/topsim.v

# Make the instruction signal a top-level input to be selected by the
# model checker
patch -i ./step1-topsim-changes.patch ../ridecore-src-buggy/topsim.v

# Instantiate the instruction-constraint module to constrain the
# instruction to be a valid instruction from the ISA
patch -i ./step2-topsim-changes.patch ../ridecore-src-buggy/topsim.v

# Update the pipeline module to wire up the QED module

# Drive instruction signal from top-level input, instantiate the QED
# module to modify instructions, send the output instruction of the
# QED module through the pipeline
patch -i ./step0-pipeline-changes.patch ../ridecore-src-buggy/pipeline.v

# OPTIONAL: make additional modifications to speed up model checking

# Disable branch prediction

patch -i ./step0-pipeline_if-changes-optimization.patch ../ridecore-src-buggy/pipeline_if.v

# Reduce size of memory

patch -i ./step0-dmem-changes-optimization.patch ../ridecore-src-buggy/dmem.v

# Limit instruction fetch to only one instruction

patch -i ./step1-pipeline-changes-optimization.patch ../ridecore-src-buggy/pipeline.v

cd ..
