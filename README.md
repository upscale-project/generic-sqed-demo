# Demo: A Generic Approach to Symbolic Quick Error Detection (QED)

This demo is a reimplementation of a [previous related
demo](https://github.com/makaimann/ride-core-demo) that shows how a
bug in the [RIDECORE](https://github.com/ridecore/ridecore) RISC-V
processor core is discovered using symbolic quick error detection
(QED).

In contrast to the previous one, this demo is based on a _generic QED
module_. Given a specification of the ISA and the design in a
particular format, we generate the Verilog sources of a QED module
that is integrated in the RIDECORE design for testing purposes.

# License
This demo consists of multiple components each of which come with their own license. Please view the license files in the sub-directories. For convenience, they have been linked here: 
* Model checker and its configuration files -- ./cosa-problem-files/: [BSD LICENSE](./cosa-problem-files/LICENSE)
* RIDECORE source files -- ./ridecore-src-buggy/: [Tokyo Institute of Technology and Regents of the University of California LICENSE](./ridecore-src-buggy/LICENSE)
* QED module -- ./generic-sqed-module/: [Academic](./generic-sqed-module/LICENSE-Academic) and [Government Use Only](./generic-sqed-module/LICENSE-GOV)

# Dependencies

We assume that the [Yosys Open Synthesis Suite](https://github.com/YosysHQ/yosys), the model checker
[CoSA](https://github.com/cristian-mattarei/CoSA) and the SMT solver
[Boolector](https://github.com/Boolector/boolector) including its
Python bindings are installed.

General installation instructions can be found in the
[README](https://github.com/makaimann/ride-core-demo/blob/master/install/README.md)
of the [related demo](https://github.com/makaimann/ride-core-demo).

# Symbolic Quick Error Detection (QED)

This description has been taken from the [related demo](https://github.com/makaimann/ride-core-demo).

Symbolic Quick Error Detection (SQED) is a technique for logic bug detection and localization.
Quick Error Detection (QED) is an approach for identifying bugs (primarily in processors but it can also be used 
for other components) which transforms a set of original tests into QED checks. This involves splitting
the register file in half and using one half for the original instructions and the second half for a duplicated
sequence of instructions. Both the original and duplicated sequences execute the same instructions in the same order, 
but they are interleaved. After the original and duplicate instruction sequences complete, the two halves of the 
register file should match. Empirically, this approach can reduce the length of bug traces by up to 6 orders of 
magnitude when compared to traditional techniques.

_Symbolic_ QED is based on the observation that a Bounded Model Checker can _symbolically_ explore all instruction 
sequences (up to a bound). Notably, this gives us a way to verify a processor without writing tests, and without even 
providing any handwritten properties, instead relying only on this symbolic QED check. 
For a much more in depth introduction, see this [paper](https://arxiv.org/pdf/1711.06541.pdf).

# Directory Tree

- ridecore-src-buggy: RIDECORE source files are obtained
  from [GitHub](https://github.com/ridecore/ridecore) and commit
  112a9bf24bf137344e89436c930c8d1220aaef60 (one off master) which
  still has the bug in the multiply decoder bug. The bug was fixed officially in [commit 200c6a663e01cb2231004bb2543e7ce8b1c92cca](https://github.com/ridecore/ridecore/commit/200c6a663e01cb2231004bb2543e7ce8b1c92cca). This demo shows how
  we detect that bug using the generic QED module generated from an
  ISA specification file.

- cosa-problem-files: CoSA problem files for running
  symbolic QED on the RIDECORE design.
  
  - problem.txt: basic set up for the model checking run using
    CoSA. This configuration uses a reset procedure (see file
    reset_procedure.ets) to start the instruction sequence in a reset
    state. Running the reset procedure followed by the instruction
    sequence to detect the bug requires to unroll the design for a
    total number of 13 steps.
    
  - problem-use-init-state.txt: same as problem.txt but uses a
    predefined reset state (see file init.ssts), which allows to avoid running the reset
    procedure. Consequently, it is sufficient to unroll the design
    only for 10 steps to detect the bug.

  - property.txt: the actual QED property being checked (pairs of
    mapped original and duplicate registers must contain the same
    value).
    
  - init.ssts: a given initial state (reset state) where the
    instruction sequence starts. Variables not listed have a default
    value of 0.
    
  - reset_procedure.ets: procedure to bring the RIDECORE model in a
    reset state where the instruction sequence starts.
    
  - ridecore.vlist: list of Verilog source files to construct a
    symbolic model of the RIDECORE design.

- generic-sqed-module: contains a workflow to generate the
  Verilog sources of a QED module for RIDECORE. The workflow is
  implemented in Python, and for convenience the related files were copied
  from the [official (private) repository](https://github.com/upscale-project/generic-sqed-module).

  - TO BE REMOVED---directory "generic-sqed-module/QEDFiles-bug-fix/":
    contains generated QED source files that were updated to fix a spurious
    counterexample when checking RIDECORE. This directory will be
    removed once the bug has been fixed upstream in the original
    repository of the generic QED module workflow. The workflow will
    then generate the fixed source files rightaway.

- qed-wireup-patches: patch files used to modify the
  RIDECORE sources to wire up the generated QED module. Additional
  patches are applied to reduce the time required for model checking.

- qed-wireup-patches: patch file to fix the bug in
  RIDECORE detected by symbolic QED. Applying the patch file is
  equivalent to the [official bug
  fix](https://github.com/ridecore/ridecore/commit/200c6a663e01cb2231004bb2543e7ce8b1c92cca).


# Demo Workflow

- run `./generate-qed-files.sh` to generate the Verilog sources of the generic QED module for RIDECORE

- run `./wire-up-qed-module.sh` to wire up the QED module to the RIDECORE design and apply simplifications to speed up model checking

- run `CoSA --problems ./cosa-problem-files/problem-use-init-state.txt -v 2` to run model checking
  starting from a predefined reset state (will unroll to k=10) or `CoSA --problems ./cosa-problem-files/problem.txt -v 2` to apply
  a reset procedure instead of the predefined reset state (will unroll to k=13).

- CoSA produces a bug trace in terms of a VCD file `trace[1]-QED_0.vcd` that can be inspected, e.g., using GTKWave.

- fix the bug by running `fix-ridecore-bug.sh`

- running CoSA again will not find any bug within the bounds of the chosen unrolling depths (k=10 or k=13).
