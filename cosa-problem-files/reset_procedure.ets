# opcode = 7'b1111111 is a NOP
I: reset_done = False
I: reset_x = 0_1
I: opcode = 127_7

S1: reset_done = False
S1: reset_x = 0_1
S1: opcode = 127_7

S2: reset_done = False
S2: reset_x = 0_1
S2: opcode = 127_7

S3: reset_done = True
S3: reset_x = 1_1

# TRANS
I -> S1
S1 -> S2
S2 -> S3
S3 -> S3
