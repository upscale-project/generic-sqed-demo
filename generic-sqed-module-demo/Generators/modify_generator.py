import sys
sys.path.append("../FormatParsers/")
sys.path.append("../Interface/")
import format_parser as P
import module_interface as I

# Verilog file
verilog = ""

# Parse the input format file
format_sections, format_dicts = P.parse_format("../FormatFiles/RV32M-ridecore_format.txt")

# Get ISA information
isa_info = format_dicts["ISA"]
# Get constraints for qed module setup
qed_constraints = format_dicts["QEDCONSTRAINTS"]
# Get register names
registers = format_dicts["REGISTERS"]
# Get instruction types requirements
ins_reqs = format_dicts["INSREQS"]
# Get the instruction fields for each type
ins_fields = format_dicts["INSFIELDS"]
# Get the bit fields
bit_fields = format_dicts["BITFIELDS"]
# Get all instruction types
instructions = {}
for ins in format_dicts["INSTYPES"].keys():
    if ins != "CONSTRAINT":
        instructions[ins] = format_dicts[ins]

MODULENAME = "modify_instruction"
INPUTS = {"qic_qimux_instruction": int(isa_info["instruction_length"])}
OUTPUTS = {"qed_instruction": int(isa_info["instruction_length"])}

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
    verilog += I.signal_def(OUTPUTS[out], "output", out, num_spaces=2)
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

# Temporary fix
verilog += I.signal_def(12, "wire", "NEW_imm12", num_spaces=2)
verilog += I.newline(1)
verilog += I.signal_def(7, "wire", "NEW_imm7", num_spaces=2)
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
            new_reg = I.bit_vector(["1'b1", I.signal_index(reg, str(bits-2), "0")])
            cond = I.inline_conditional(equals_zero, reg, new_reg, False)
            verilog += I.assign_def("NEW_"+reg, cond, num_spaces=2)
            verilog += I.newline(1)
            modified_fields.append(reg)

# Temporary fix
verilog += I.assign_def("NEW_imm12", I.bit_vector(["2'b01", I.signal_index("imm12", "9", "0")]), num_spaces=2)
verilog += I.newline(1)
modified_fields.append("imm12")
verilog += I.assign_def("NEW_imm7", I.bit_vector(["2'b01", I.signal_index("imm7", "4", "0")]), num_spaces=2)
verilog += I.newline(1)
modified_fields.append("imm7")

# Assign the new instruction types with the modified fields
verilog += I.newline(1)
for ins_type in ins_reqs:
    if ins_type != "CONSTRAINT":
        fields = ins_fields[ins_type].split()
        new_fields = []
        for field in fields:
            if field in modified_fields:
                new_fields.append("NEW_"+field)
            else:
                new_fields.append(field)
        verilog += I.assign_def("INS_"+ins_type, I.bit_vector(new_fields), num_spaces=2)
        verilog += I.newline(1)

# Assign the final qed instruction output after modification
verilog += I.newline(1)
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

# Module footer
verilog += I.newline(1)
verilog += I.module_footer()

f = open("../QEDFiles/modify_instruction.v", 'w')
f.write(verilog)
f.close()









