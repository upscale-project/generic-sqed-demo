# Copyright (c) Stanford University
#
# This source code is patent protected and being made available under the
# terms explained in the ../LICENSE-Academic and ../LICENSE-GOV files.

# Author: Mario J Srouji
# Email: msrouji@stanford.edu

import copy
import os
from shutil import copyfile
import sys
sys.path.append("../FormatParsers/")
sys.path.append("../Interface/")

import format_parser as P
import module_interface as I

# Format file
try:
    INFILE = sys.argv[1]
except:
    print("ERROR: Please provide the format file path as the first argument.")
    quit()
# Output directory
try:
    OUTFILE = sys.argv[2]
    if not os.path.isdir(OUTFILE):
        os.mkdir(OUTFILE)
    if OUTFILE[-1] != "/":
        OUTFILE = OUTFILE + "/"
    copyfile("../QEDFiles/qed_i_cache.v", OUTFILE+"qed_i_cache.v")
    copyfile("../QEDFiles/qed_instruction_mux.v", OUTFILE+"qed_instruction_mux.v")
    print("MESSAGE: Created directory "+OUTFILE+" and moved mux and cache files.")
except:
    OUTFILE = "../QEDFiles/"
    print("MESSAGE: Using default directory QEDFiles as output directory.")
# SIC COSA OPS
try:
    OPSFILE = sys.argv[3]
except:
    OPSFILE = None
    print("MESSAGE: SIC Cosa operator file was not provided. Omitting SIC generation.")

# LICENSE file to be included as header for all generated files
try:
    f = open("LICENSE.v", 'r')
    license_header = f.read() + "\n"
    f.close()
except:
    print("MESSAGE: Unable to read LICENSE.v file, please include user license information.")
    quit()

# Grabs all global ISA format information
format_sections, format_dicts = P.parse_format(INFILE)

# Currently, these are required for the SQED generators.
needed_sections = ["ISA", "REGISTERS", "MEMORY", 
                   "QEDCONSTRAINTS", "INSTYPES",
                   "INSFIELDS", "INSREQS", 
                   "BITFIELDS"]
found_sections = [False]*len(needed_sections)

try:
    # Get ISA information
    isa_info = format_dicts["ISA"]
    found_sections[0] = True
    # Get register names
    registers = format_dicts["REGISTERS"]
    found_sections[1] = True
    # Get memory fields needed for modification
    memory = format_dicts["MEMORY"]
    found_sections[2] = True
    # Get constraints for qed module setup
    qed_constraints = format_dicts["QEDCONSTRAINTS"]
    found_sections[3] = True
    # Get the instruction types
    ins_types = format_dicts["INSTYPES"]
    found_sections[4] = True
    # Get the instruction fields for each type
    ins_fields = format_dicts["INSFIELDS"]
    found_sections[5] = True
    # Get instruction types requirements
    ins_reqs = format_dicts["INSREQS"]
    found_sections[6] = True
    # Get the bit fields
    bit_fields = format_dicts["BITFIELDS"]
    found_sections[7] = True
    # Get all instruction types
    instructions = {}
    for ins in format_dicts["INSTYPES"].keys():
        if ins != "CONSTRAINT":
            instructions[ins] = format_dicts[ins]
except:
    not_found = found_sections.index(False)
    print("ERROR: Format file is missing necessary section: "+needed_sections[not_found])
    quit()

# SIC files 
if not OPSFILE is None:
    try:
        from SIC_generator import *
        generate_SIC_files(format_dicts, OPSFILE)
        print("MESSAGE: Generated and wrote single instruction check files.")
    except:
        print("ERROR: Unable to generate SIC files.")

# Constraints file
try:
    from constraint_generator import *
    MODULENAME = "inst_constraint"
    INPUTS = {"clk": 1, "instruction": int(isa_info["instruction_length"])}
    OUTPUTS = {}
except:
    print("ERROR: Missing or non-integer instruction_length field in ISA section.")
    quit()

try:
    verilog = generate_constraints_file(MODULENAME, INPUTS, OUTPUTS, format_dicts)
except:
    print("ERROR: Unable to generate constraints file.")

try:
    f = open(OUTFILE+"inst_constraints.v", 'w')
    f.write(license_header+verilog)
    f.close()
    print("MESSAGE: Generated and wrote constraints file.")
except:
    print("ERROR: Unable to write constraints file.")

# Decoder file
from decoder_generator import *

MODULENAME = "qed_decoder"
INPUTS = {"ifu_qed_instruction": int(isa_info["instruction_length"])}
OUTPUTS = {}

try:
    verilog = generate_decoder_file(MODULENAME, INPUTS, OUTPUTS, format_dicts)
except:
    print("ERROR: Unable to generate decoder file.")    
    
try:
    f = open(OUTFILE+"qed_decoder.v", 'w')
    f.write(license_header+verilog)
    f.close()
    print("MESSAGE: Generated and wrote decoder file.")
except:
    print("ERROR: Unable to write decoder file.")

# Modify file
from modify_generator import *

MODULENAME = "modify_instruction"
INPUTS = {"qic_qimux_instruction": int(isa_info["instruction_length"])}
OUTPUTS = {"qed_instruction": int(isa_info["instruction_length"])}

try:
    verilog = generate_modify_file(MODULENAME, INPUTS, OUTPUTS, format_dicts)
except:
    print("ERROR: Unable to generate modify file.")

try:
    f = open(OUTFILE+"modify_instruction.v", 'w')
    f.write(license_header+verilog)
    f.close()
    print("MESSAGE: Generated and wrote modify file.")
except:
    print("ERROR: Unable to write modify file.")

# QED top file
from qed_generator import *

MODULENAME = "qed"
INPUTS = {"clk": 1, "ifu_qed_instruction": int(isa_info["instruction_length"]),
                "rst": 1, "ena": 1, "exec_dup": 1, "stall_IF": 1}
OUTPUTS = {"qed_ifu_instruction": int(isa_info["instruction_length"]), "vld_out": 1}

try:
    verilog = generate_qed_file(MODULENAME, INPUTS, OUTPUTS, format_dicts)
except:
    print("ERROR: Unable to generate modify file.")

try:
    f = open(OUTFILE+"qed.v", 'w')
    f.write(license_header+verilog)
    f.close()
    print("MESSAGE: Generated and wrote top-level qed file.")
except:
    print("ERROR: Unable to write top-level qed file.")



