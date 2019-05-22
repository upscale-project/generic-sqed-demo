# generic-sqed-demo

TO BE UPDATED AND POLISHED

TODO: add appropriate license files for QED generator files, generated files and ridecore

- directory "ridecore-src-buggy": ridecore source files are obtained
  from GitHub at https://github.com/ridecore/ridecore and commit
  112a9bf24bf137344e89436c930c8d1220aaef60 (one off master) which
  still has the bug in the multiply decoder bug. This demo shows how
  we detect that bug using the generic QED module generated from an
  ISA specification file

- directory "cosa-problem-files": CoSA problem files for running
  SQED. These files are the same as in the San Diego demo, except for
  file 'ridecore.vlist' which has been adapted to new paths.

- directory "generic-sqed-module": contains a workflow to generate the
  Verilog sources of a QED module for ridecore. The workflow is
  implemented in Python, and for convenience the related files were copied
  from the official (private) repository at
  https://github.com/upscale-project/generic-sqed-module

- TO BE REMOVED--- directory "generic-sqed-module/QEDFiles-bug-fix/":
  contains QED source files that were updated to fix a spurious
  counterexample when checking ridecore. This directory will be
  removed once the bug has been fixed upstream in the original
  repository of the generic QED module workflow. The workflow will
  then generate the fixed source files rightaway.

