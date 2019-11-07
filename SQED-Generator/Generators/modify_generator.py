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

def generate_modify_file(MODULENAME, INPUTS, OUTPUTS, format_dicts):
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

    # Fill out the INPUTS dict
    for bit_field in bit_fields:
        if bit_field != "CONSTRAINT":
            msb, lsb = bit_fields[bit_field].split()
            bits = int(msb) - int(lsb) + 1
            INPUTS[bit_field] = bits

    for ins_type in instructions:
        if ins_type in ins_reqs:
            INPUTS["IS_"+ins_type] = 1

    verilog += I.module_header(MODULENAME, INPUTS, OUTPUTS)
    verilog += I.newline(2)

    # Instantiate inputs
    for inp in INPUTS:
        verilog += I.signal_def(INPUTS[inp], "input", inp, num_spaces=2)
        verilog += I.newline(1)

    # Instantiate outputs
    verilog += I.newline(1)
    for out in OUTPUTS:
        verilog += I.signal_def(OUTPUTS[out], "output reg", out, num_spaces=2)
        verilog += I.newline(1)

    # Instantiate new instruction types wires
    verilog += I.newline(1)
    for ins_type in ins_reqs:
        verilog += I.signal_def(int(isa_info["instruction_length"]), "wire", "INS_"+ins_type, num_spaces=2)
        verilog += I.newline(1)

    # Instantiate the new registers and immediate values
    verilog += I.newline(1)
    if qed_constraints["half_registers"] == "1":
        for reg in registers:
            if reg != "CONSTRAINT":
                msb, lsb = bit_fields[reg].split()
                bits = int(msb) - int(lsb) + 1
                verilog += I.signal_def(bits, "wire", "NEW_"+reg, num_spaces=2)
                verilog += I.newline(1)

    if qed_constraints["half_memory"] == "1":
        for mem in memory:
            if mem != "CONSTRAINT":
                msb, lsb = bit_fields[mem].split()
                bits = int(msb) - int(lsb) + 1
                verilog += I.signal_def(bits, "wire", "NEW_"+mem, num_spaces=2)
                verilog += I.newline(1)

    # Keeps track of modified fields
    modified_fields = []

    # Assign the new values for the registers
    verilog += I.newline(1)
    if qed_constraints["half_registers"] == "1":
        for reg in registers:
            if reg != "CONSTRAINT":
                msb, lsb = bit_fields[reg].split()
                bits = int(msb) - int(lsb) + 1
                equals_zero = I._equals(reg, I._constant(bits, "0"*bits), True)
                new_reg = I.bit_vector([I._constant(1, "1"), I.signal_index(reg, str(bits-2), "0")])
                cond = I.inline_conditional(equals_zero, reg, new_reg, False)
                verilog += I.assign_def("NEW_"+reg, cond, num_spaces=2)
                verilog += I.newline(1)
                modified_fields.append(reg)

    if qed_constraints["half_memory"] == "1":
        for mem in memory:
            if mem != "CONSTRAINT":
                msb, lsb = bit_fields[mem].split()
                bits = int(msb) - int(lsb) + 1
                new_mem = I.bit_vector([I._constant(2, "01"), I.signal_index(mem, str(bits-3), "0")])
                verilog += I.assign_def("NEW_"+mem, new_mem)
                verilog += I.newline(1)
                modified_fields.append(mem)

    # Assign the new instruction types with the modified fields
    verilog += I.newline(1)
    if len(ins_types["CONSTRAINT"]) > 0:
        ins_types_defs = {}
        for c in ins_types["CONSTRAINT"]:
            parts = c.split(",")
            ins_types_defs[parts[0]] = parts[1:]

        mem_types = ins_types_defs["MEMORYTYPE"]
    else:
        mem_types = []

    for ins_type in ins_reqs:
        if ins_type != "CONSTRAINT":
            fields = ins_fields[ins_type].split()
            new_fields = []
            for field in fields:
                if ((field in modified_fields and field in registers) or
                    (field in modified_fields and field in memory and ins_type in mem_types)):
                    new_fields.append("NEW_"+field)
                else:
                    new_fields.append(field)
            verilog += I.assign_def("INS_"+ins_type, I.bit_vector(new_fields), num_spaces=2)
            verilog += I.newline(1)

    # Assign the final qed instruction output after modification
    verilog += I.newline(1)
    output_instruction = OUTPUTS.keys()[0]
    types = ins_reqs.keys()
    types.remove("CONSTRAINT")
    conditional = ""
    for i in range(len(types)):
        ins_type = types[i]
        if i < len(types) - 1:
            false = "("
        else:
            false = "qic_qimux_instruction"
        conditional += I.inline_conditional("IS_"+ins_type, "INS_"+ins_type, false, False)
    conditional += (len(types) - 1) * ")"
    verilog += I.assign_def(output_instruction, conditional, num_spaces=2)
    verilog += I.newline(1)

    # This code does the same thing as above, 
    # but utilizes the always_comb logic
    # to make it more readable. However
    # this will cause certain verilog compilers
    # to complain.
    """
    verilog += I.always_comb_def(num_spaces=2)
    verilog += I.newline(1)
    output_instruction = OUTPUTS.keys()[0]
    types = ins_reqs.keys()
    types.remove("CONSTRAINT")
    for i in range(len(types)+1):
        if i == 0:
            ins_type = types[i]
            verilog += I.if_header("IS_"+ins_type, num_spaces=4)
        elif i < len(types):
            ins_type = types[i]
            verilog += I.else_if_header("IS_"+ins_type, num_spaces=4)
        else:
            verilog += I.else_header(num_spaces=4)
            verilog += I.newline(1)
            verilog += I.direct_assignment_def(output_instruction, "qic_qimux_instruction", num_spaces=6)
            verilog += I.newline(1)
            verilog += I.end(num_spaces=4)
            verilog += I.newline(1)
            continue

        verilog += I.newline(1)
        verilog += I.direct_assignment_def(output_instruction, "INS_"+ins_type, num_spaces=6)
        verilog += I.newline(1)
        verilog += I.end(num_spaces=4)
        verilog += I.newline(1)
    verilog += I.end(num_spaces=2)
    verilog += I.newline(1)
    """

    # Module footer
    verilog += I.newline(1)
    verilog += I.module_footer()

    return verilog









