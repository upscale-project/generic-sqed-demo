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
# Get instruction types requirements
ins_reqs = format_dicts["INSREQS"]
# Get the bit fields
bit_fields = format_dicts["BITFIELDS"]
# Get all instruction types
instructions = {}
for ins in format_dicts["INSTYPES"].keys():
    if ins != "CONSTRAINT":
        instructions[ins] = format_dicts[ins]

MODULENAME = "qed_decoder"
INPUTS = {"ifu_qed_instruction": int(isa_info["num_registers"])}
OUTPUTS = {}

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
    reqs = []
    for req in ins_req:
        if req != "CONSTRAINT":
            reqs.append(I._equals(req, I._constant(len(ins_req[req]), ins_req[req]), parens=True))

    reqs_expression = reqs[0]
    for i in range(1, len(reqs)):
        reqs_expression = I._and(reqs_expression, reqs[i], parens=False)

    verilog += I.assign_def("IS_"+ins_type, reqs_expression, num_spaces=2)
    verilog += I.newline(1)

# Module footer
verilog += I.newline(1)
verilog += I.module_footer()

f = open("../QEDFiles/qed_decoder.v", 'w')
f.write(verilog)
f.close()









