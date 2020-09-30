# Demo: A Generic Approach to Symbolic Quick Error Detection (QED)

This demo is a re-implementation of a [previous related
demo](https://github.com/makaimann/ride-core-demo) that shows how a
bug in the [RIDECORE](https://github.com/ridecore/ridecore) RISC-V
processor core is discovered using symbolic quick error detection
(SQED).

In contrast to the previous one, this demo is based on a _generic QED
module_. Given a specification of the ISA and the design in a
particular format, we generate the Verilog sources of a QED module
that is integrated in the RIDECORE design for testing purposes.

# Demo Video

Our workflow is illustrated in the following [demo video](http://upscale.stanford.edu/materials/eri-summit-2019-sqed-demo-video.mp4) prepared for the [ERI Summit 2019](http://www.eri-summit.com/). The demo shows the same general workflow but runs the model checker [CoSA](https://github.com/cristian-mattarei/CoSA) instead of the newer version [Pono](https://github.com/upscale-project/pono).

# License
This demo consists of multiple components each of which comes with its own license. Please view the license files in the sub-directories. For convenience, they have been linked here:
* Yosys and scripts -- setup-yosys.sh, gen-btor.ys: [ISC LICENSE](https://github.com/YosysHQ/yosys/blob/master/COPYING)
* Model checker and scripts -- setup-pono.sh, run-pono.sh: [BSD LICENSE](./BSD_LICENSE)
* RIDECORE source files -- ./ridecore-src-buggy/: [Tokyo Institute of Technology and Regents of the University of California LICENSE](./ridecore-src-buggy/LICENSE)
* QED module -- ./generic-sqed-module-demo/:
[Academic](./generic-sqed-module-demo/LICENSE-Academic) and
[Government](./generic-sqed-module-demo/LICENSE-GOV) use only.  SQED is patent
protected and may not be used for commercial purposes or any other purposes outside the conditions of these two licenses.

# Dependencies

We assume that the [Yosys Open Synthesis
Suite](https://github.com/YosysHQ/yosys), and the model checker
[Pono](https://github.com/upscale-project/pono) are installed. For convenience,
we have provided the setup scripts `setup-yosys.sh`, and `setup-pono.sh`.
However, both assume their dependencies are installed. Please see the relevant
repositories for that information. Alternatively, there is a Dockerfile in
`docker` for running this demo in Docker.

## Docker
* [Docker installation](https://hub.docker.com/search/?type=edition&offering=community)
* On linux, you will probably need to preface every docker command with `sudo`. Unless you take extra steps to avoid this.
* To build the image, run `docker build -t <name of your choice> <path to the directory with Dockerfile>`
  * For example, `docker build -t sqed ./docker`
  * It will take a while to build the image with all the dependencies
*  Now you can start the image with ``docker run -it --rm -v `pwd`/data:/home/sqed-demo/generic-sqed-demo/data <name of image>``
  * For example, ``docker run -it --rm -v `pwd`/data:/home/sqed-demo/generic-sqed-demo/data sqed``
* The `data` directory is for shared data, which can be accessed both from within the container and in the host
  * This can be used to share a waveform and then view it on the host machine
* We use [gtkwave](http://gtkwave.sourceforge.net/) for viewing waveforms

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
  to detect that bug using the generic QED module generated from an
  ISA specification file.

- generic-sqed-module-demo: contains a workflow to generate the
  Verilog sources of a QED module for RIDECORE. The workflow is
  implemented in Python.

- qed-wireup-patches: patch files used to modify the
  RIDECORE sources to wire up the generated QED module. Additional
  patches are applied to reduce the time required for model checking.

- qed-wireup-patches: patch file to fix the bug in
  RIDECORE detected by symbolic QED. Applying the patch file is
  equivalent to the [official bug
  fix](https://github.com/ridecore/ridecore/commit/200c6a663e01cb2231004bb2543e7ce8b1c92cca).


# Demo Workflow

To demonstrate the application of the generic QED module, we run the following steps.

- Run the script `./generate-qed-files.sh` to generate the Verilog
  sources of the generic QED module for RIDECORE.

  - In this step, several Python scripts located in subdirectory
    `./generic-sqed-module-demo/Generators/` are executed to produce the
    sources of the QED module from the ISA/design specification file
    `generic-sqed-module-demo/FormatFiles/RV32M-ridecore_format.txt`. The
    specification file contains a structured description of the ISA
    and additional parameters of the design. It has to be set up by
    the designer. The Python scripts, however, process the
    specification file and do _not_ have to adapted to the design,
    i.e., they are generic. The QED source files generated by the
    Python scripts are put in subdirectory
    `generic-sqed-module-demo/QEDFiles`.

- Run the script `./wire-up-qed-module.sh` to wire up the QED module
  to the RIDECORE design and apply simplifications to speed up model
  checking. This step modifies the Verilog sources of RIDECORE by
  means of patch files as follows (the order in which the patch files
  are applied matters and must not be changed).

  - In the `topsim` module, pragmas are added to make sure that
    certain parts of the design are not eliminated during
    simplification when constructing the model. This step is necessary
    because Yosys, which we use in our workflow to parse Verilog
    input, would otherwise eliminate these parts.

    Furthermore, we make the `instruction` signal a top-level input of
    the design. This is necessary in order to let the model checker
    select the instruction and hence construct an instruction
    sequence. Additionally, we instantiate the `inst_constraint`
    module that is part of the QED module to make sure that the model
    checker selects only instructions that are part of the ISA.

    We also add the assumption that reset is not activated. We will
    simulate the reset sequence in Yosys, and thus can assume for
    model checking that the reset is not active.

  - We modify the `pipeline` module to drive the `instruction` signal
    from the respective top-level input and we instantiate the QED module
    to modify the instruction. Finally, we send the output instruction
    of the QED module through the pipeline instead of the instruction
    obtained in the instruction fetch stage.

    We also add outputs in `arf`, and `ram_sync_nolatch`, so that
    registers 1 and 17 are accessible in the `pipeline` where the
    QED module is. These are used in the universal property, and
    Yosys does not support referring to internal signals of modules.
    Note: the full universal property, would need to check all pairs:
    1 and 17, 2 and 18, 3 and 19, etc. For this demo, we only need
    the two and leave the others out to minimize changes.

  - Additionally, we apply the following steps, which are optional but
    crucial to reduce the amount of time required for model checking.

    - Disabling branch prediction.

    - Reducing size of data memory.

    - Fetch only one instruction in the instruction fetch stage.

    - Remove the branch target buffer (module `btb`) to get rid of
      negative-edge behavior of the clock. This optimization allows to
      abstract the clock in model checking and reduce the number of
      necessary unrollings in BMC from 24 to 13.

- Setting up the environment. If you do not already have `Yosys` installed,
  you can run `setup-yosys.sh` to build it locally. Please refer to the
  [Yosys repository](https://github.com/YosysHQ/yosys) for any dependency
  information. If you do not already have `Pono` installed, you may use
  the `setup-pono.sh` script to build it locally. Please refer to the
  [Pono repository](https://github.com/upscale-project/pono) for any
  installation information if the build fails.

- Run `run-pono.sh` to use Yosys to generate a BTOR2 file, `ridecore.btor2`,
  and then run bounded model checking with `Pono` to find the bug. It should
  get to bound 10 very quickly, but take about 10m to find the bug at bound 11.
  It will write a trace to `ridecore-trace.vcd`. Note, all of the constraints
  and the assertion are embedded in the BTOR2 file. Thus, you can use any
  model checker that reads BTOR2 to check this property.

- Fix the bug by running `fix-ridecore-bug.sh`.

- Running Pono again will not find any bug within the bounds of the
  chosen unrolling depth (k=12).
