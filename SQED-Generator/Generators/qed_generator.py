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

def generate_qed_file(MODULENAME, INPUTS, OUTPUTS, format_dicts):
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

    # Adds module header definition
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

    # Instantiate bit fields as wires
    for bit_field in bit_fields:
        if bit_field != "CONSTRAINT":
            msb, lsb = bit_fields[bit_field].split()
            bits = int(msb) - int(lsb) + 1
            verilog += I.signal_def(bits, "wire", bit_field, num_spaces=2)
            verilog += I.newline(1)

    # Instantiate new instruction types wires
    verilog += I.newline(1)
    for ins_type in ins_reqs:
        if ins_type != "CONSTRAINT":
            verilog += I.signal_def(1, "wire", "IS_"+ins_type, num_spaces=2)
            verilog += I.newline(1)

    # Instantiate internal instruction versions
    verilog += I.newline(1)
    verilog += I.signal_def(int(isa_info["instruction_length"]), "wire", "qed_instruction", num_spaces=2)
    verilog += I.newline(1)
    verilog += I.signal_def(int(isa_info["instruction_length"]), "wire", "qic_qimux_instruction", num_spaces=2)
    verilog += I.newline(2)

    # Decoder module
    decoder_args = ["qic_qimux_instruction"]
    decoder_args = decoder_args + list(bit_fields.keys())
    decoder_args.remove("CONSTRAINT")
    decoder_args = decoder_args + [("IS_"+key) for key in ins_reqs]
    decoder_args.remove("IS_CONSTRAINT")
    signals = decoder_args
    names = copy.deepcopy(signals)
    names[0] = "ifu_qed_instruction"
    verilog += I.module_def("qed_decoder", "dec", names, signals, num_spaces=2)
    verilog += I.newline(2)

    # Modify module
    modify_args = ["qed_instruction", "qic_qimux_instruction"]
    modify_args = modify_args + list(bit_fields.keys())
    modify_args.remove("CONSTRAINT")
    modify_args = modify_args + [("IS_"+key) for key in ins_reqs]
    modify_args.remove("IS_CONSTRAINT")
    signals = modify_args
    names = modify_args
    verilog += I.module_def("modify_instruction", "minst", names, signals, num_spaces=2)
    verilog += I.newline(2)

    # Mux module
    mux_args = ["qed_ifu_instruction", "ifu_qed_instruction", "qed_instruction", "exec_dup", "ena"]
    signals = mux_args
    names = mux_args
    verilog += I.module_def("qed_instruction_mux", "imux", names, signals, num_spaces=2)
    verilog += I.newline(2)

    # Cache module
    cache_args = ["qic_qimux_instruction", "vld_out", "clk", "rst", "exec_dup", "stall_IF", "ifu_qed_instruction"]
    signals = cache_args
    names = copy.deepcopy(signals)
    names[-2] = "IF_stall"
    verilog += I.module_def("qed_i_cache", "qic", names, signals, num_spaces=2)
    verilog += I.newline(2)

    verilog += I.module_footer()

    return verilog








