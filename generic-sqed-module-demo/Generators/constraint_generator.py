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
# Get register names
registers = format_dicts["REGISTERS"]
# Get constraints for qed module setup
qed_constraints = format_dicts["QEDCONSTRAINTS"]
# Get the instruction fields for each type
ins_fields = format_dicts["INSFIELDS"]
# Get the bit fields
bit_fields = format_dicts["BITFIELDS"]
# Get all instruction types
instructions = {}
for ins in format_dicts["INSTYPES"].keys():
    if ins != "CONSTRAINT":
        instructions[ins] = format_dicts[ins]

# Global header for module
MODULENAME = "inst_constraint"
INPUTS = {"clk": 1, "instruction": int(isa_info["instruction_length"])}
OUTPUTS = {}

# Adds module header definition
verilog += I.module_header(MODULENAME, INPUTS, OUTPUTS)
verilog += I.newline(2)

# Instantiate inputs
for inp in INPUTS:
    verilog += I.signal_def(INPUTS[inp], "input", inp, num_spaces=2)
    verilog += I.newline(1)

# Instantiate inputs
for out in OUTPUTS:
    verilog += I.signal_def(OUTPUTS[out], "output", out, num_spaces=2)
    verilog += I.newline(1)

# Instantiate bit fields
verilog += I.newline(1)
for bit_field in bit_fields:
    if bit_field != "CONSTRAINT":
        msb, lsb = bit_fields[bit_field].split()
        bits = int(msb) - int(lsb) + 1
        verilog += I.signal_def(bits, "wire", bit_field, num_spaces=2)
        verilog += I.newline(1)

# Instantiate instructions
verilog += I.newline(1)
for ins_type in instructions:
    #if len(instructions[ins_type]["CONSTRAINT"]) > 0:
    if ins_type != "NOP":
        verilog += I.signal_def(1, "wire", "FORMAT_"+ins_type, num_spaces=2)
        verilog += I.newline(1)
    verilog += I.signal_def(1, "wire", "ALLOWED_"+ins_type, num_spaces=2)
    verilog += I.newline(1)
    for ins in instructions[ins_type]:
        if ins != "CONSTRAINT":
            verilog += I.signal_def(1, "wire", ins, num_spaces=2)
            verilog += I.newline(1)
    verilog += I.newline(1)

# Assign bit fields
for bit_field in bit_fields:
    if bit_field != "CONSTRAINT":
        msb, lsb = bit_fields[bit_field].split()
        verilog += I.assign_def(bit_field, I.signal_index("instruction", msb, lsb), num_spaces=2)
        verilog += I.newline(1)

# Assign instruction types
verilog += I.newline(1)
for ins_type in instructions:
    type_constraints = instructions[ins_type]["CONSTRAINT"]
    constraints = []

    if qed_constraints["half_registers"] == "1":
        fields = ins_fields[ins_type].split()
        for field in fields:
            if field in registers:
                constraints.append(I._lt(field, str(int(isa_info["instruction_length"])/2), parens=True))

    for type_constraint in type_constraints:
        constraints.append(type_constraint)

    if ins_type != "NOP" and len(constraints) > 0:
        expression = constraints[0]
        for i in range(1, len(constraints)):
            expression = I._and(expression, constraints[i], parens=False)

        verilog += I.assign_def("FORMAT_"+ins_type, expression, num_spaces=2)
        verilog += I.newline(1)

    allowed_expression = ""
    for ins in instructions[ins_type]:
        if ins != "CONSTRAINT":
            fields = instructions[ins_type][ins]
            reqs = []
            for field in fields:
                if field != "CONSTRAINT":
                    req = fields[field]
                    reqs.append(I._equals(field, I._constant(len(req), req), parens=True))

            #if len(instructions[ins_type]["CONSTRAINT"]) > 0:
            if ins != "NOP":
                reqs_expression = "FORMAT_" + ins_type
                for i in range(len(reqs)):
                    reqs_expression = I._and(reqs_expression, reqs[i], parens=False)
            else:
                reqs_expression = reqs[0]
                for i in range(1, len(reqs)):
                    reqs_expression = I._and(reqs_expression, reqs[i], parens=False)

            verilog += I.assign_def(ins, reqs_expression, num_spaces=2)
            verilog += I.newline(1)

            if allowed_expression == "":
                allowed_expression = ins
            else:
                allowed_expression = I._or(allowed_expression, ins, parens=False)

    verilog += I.assign_def("ALLOWED_"+ins_type, allowed_expression, num_spaces=2)
    verilog += I.newline(2)

# Property assertion
assertions = instructions.keys()
property_expression = ""
for ins_type in assertions:
    if property_expression == "":
        property_expression = "ALLOWED_" + ins_type
    else:
        property_expression = I._or(property_expression, "ALLOWED_"+ins_type, parens=False)

verilog += I.always_def("clk", num_spaces=2) + I.begin(num_spaces=1)
verilog += I.newline(1)
verilog += I.property_def(property_expression, num_spaces=4)
verilog += I.newline(1)
verilog += I.end(num_spaces=2)
verilog += I.newline(1)

# End module with footer
verilog += I.newline(1)
verilog += I.module_footer()

f = open("../QEDFiles/inst_constraints.v", 'w')
f.write(verilog)
f.close()









