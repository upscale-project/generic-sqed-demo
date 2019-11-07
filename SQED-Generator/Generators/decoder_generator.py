# Copyright (c) Stanford University
#
# This source code is patent protected and being made available under the
# terms explained in the ../LICENSE-Academic and ../LICENSE-GOV files.

# Author: Mario J Srouji
# Email: msrouji@stanford.edu

import copy
import sys
sys.path.append("../FormatParsers/")
sys.path.append("../Interface/")

import format_parser as P
import module_interface as I

def generate_decoder_file(MODULENAME, INPUTS, OUTPUTS, format_dicts):
    # Get ISA information
    isa_info = format_dicts["ISA"]
    # Get register names
    registers = format_dicts["REGISTERS"]
    # Get memory fields needed for modification
    memory = format_dicts["MEMORY"]
    # Get constraints for qed module setup
    qed_constraints = format_dicts["QEDCONSTRAINTS"]
    # Get the instruction types
    ins_types = format_dicts["INSTYPES"]
    # Get the instruction fields for each type
    ins_fields = format_dicts["INSFIELDS"]
    # Get instruction types requirements
    ins_reqs = format_dicts["INSREQS"]
    # Get the bit fields
    bit_fields = format_dicts["BITFIELDS"]
    # Get all instruction types
    instructions = {}
    for ins in format_dicts["INSTYPES"].keys():
            if ins != "CONSTRAINT":
                        instructions[ins] = format_dicts[ins]

    # Verilog file
    verilog = ""

    # Fill out the OUTPUTS dict
    for bit_field in bit_fields:
        if bit_field != "CONSTRAINT":
            msb, lsb = bit_fields[bit_field].split()
            bits = int(msb) - int(lsb) + 1
            OUTPUTS[bit_field] = bits

    for ins_type in instructions:
        if ins_type in ins_reqs:
            OUTPUTS["IS_"+ins_type] = 1

    # Header for module
    verilog += I.module_header(MODULENAME, INPUTS, OUTPUTS)
    verilog += I.newline(2)

    # Instantiate inputs
    for inp in INPUTS:
        verilog += I.signal_def(INPUTS[inp], "input", inp, num_spaces=2)
        verilog += I.newline(1)

    # Instantiate outputs
    verilog += I.newline(1)
    for out in OUTPUTS:
        verilog += I.signal_def(OUTPUTS[out], "output", out, num_spaces=2)
        verilog += I.newline(1)

    # Assign the bit fields to the correct bits in instruction
    verilog += I.newline(1)
    for bit_field in bit_fields:
        if bit_field != "CONSTRAINT":
            msb, lsb = bit_fields[bit_field].split()
            verilog += I.assign_def(bit_field, I.signal_index(INPUTS.keys()[0], msb, lsb), num_spaces=2)
            verilog += I.newline(1)

    # Assign instruction types requirements
    verilog += I.newline(1)
    for ins_type in instructions:
        if not ins_type in ins_reqs:
            continue
        ins_req = ins_reqs[ins_type]
        reqs = ins_req["CONSTRAINT"]
        for field in ins_req:
            if field != "CONSTRAINT":
                if type(ins_req[field]) == type([]):
                    first = ins_req[field][0]
                    req_expression = I._equals(field, I._constant(len(first), first), parens=True)
                    for req in ins_req[field][1:]:
                        equality = I._equals(field, I._constant(len(req), req), parens=True)
                        req_expression = I._or(req_expression, equality, parens=False)
                    req_expression = "(" + req_expression + ")"
                    reqs.append(req_expression)
                else:
                    equality = I._equals(field, I._constant(len(ins_req[field]), ins_req[field]), parens=True)
                    reqs.append(equality)

        reqs_expression = reqs[0]
        for i in range(1, len(reqs)):
            reqs_expression = I._and(reqs_expression, reqs[i], parens=False)

        verilog += I.assign_def("IS_"+ins_type, reqs_expression, num_spaces=2)
        verilog += I.newline(1)

    # Module footer
    verilog += I.newline(1)
    verilog += I.module_footer()

    return verilog









