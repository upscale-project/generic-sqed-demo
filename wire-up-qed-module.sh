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

# Use assumption to embed constraint that there's no reset in the BTOR2
# reset sequence will be simulated before BTOR2 generated
patch -i ./step3-topsim-changes.patch ../ridecore-src-buggy/topsim.v

# Update the pipeline module to wire up the QED module

# Drive instruction signal from top-level input, instantiate the QED
# module to modify instructions, send the output instruction of the
# QED module through the pipeline
patch -i ./step0-pipeline-changes.patch ../ridecore-src-buggy/pipeline.v

# wire registers 1 and 17 out of regfile so we can access them
# in standard Verilog (Yosys doesn't support . notation for reaching into modules)
patch -i ./step0-ram_sync_nolatch-changes.patch ../ridecore-src-buggy/ram_sync_nolatch.v
patch -i ./step0-arf-changes.patch ../ridecore-src-buggy/arf.v
patch -i ./step1-pipeline-changes.patch ../ridecore-src-buggy/pipeline.v

# OPTIONAL: make additional modifications to speed up model checking

# Disable branch prediction

patch -i ./step0-pipeline_if-changes-optimization.patch ../ridecore-src-buggy/pipeline_if.v

# Reduce size of memory

patch -i ./step0-dmem-changes-optimization.patch ../ridecore-src-buggy/dmem.v

# Limit instruction fetch to only one instruction

patch -i ./step2-pipeline-changes-optimization.patch ../ridecore-src-buggy/pipeline.v

# Remove branch target buffer to get rid of neg-edge behavior. This
# optimization allows to abstract the clock and reduce the number of
# unrollings in BMC
patch -i ./step1-pipeline_if-changes-optimization.patch ../ridecore-src-buggy/pipeline_if.v

cd ..
