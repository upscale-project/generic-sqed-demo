module qed_decoder (
// Outputs
shamt,
IS_SW,
imm12,
IS_R,
rd,
funct3,
opcode,
rs2,
funct7,
IS_I,
IS_LW,
imm5,
rs1,
imm7,
// Inputs
ifu_qed_instruction);

  input [31:0] ifu_qed_instruction;

  output [4:0] shamt;
  output IS_SW;
  output [11:0] imm12;
  output IS_R;
  output [4:0] rd;
  output [2:0] funct3;
  output [6:0] opcode;
  output [4:0] rs2;
  output [6:0] funct7;
  output IS_I;
  output IS_LW;
  output [4:0] imm5;
  output [4:0] rs1;
  output [6:0] imm7;

  assign shamt = ifu_qed_instruction[24:20];
  assign imm12 = ifu_qed_instruction[31:20];
  assign rd = ifu_qed_instruction[11:7];
  assign funct3 = ifu_qed_instruction[14:12];
  assign opcode = ifu_qed_instruction[6:0];
  assign imm7 = ifu_qed_instruction[31:25];
  assign funct7 = ifu_qed_instruction[31:25];
  assign imm5 = ifu_qed_instruction[11:7];
  assign rs1 = ifu_qed_instruction[19:15];
  assign rs2 = ifu_qed_instruction[24:20];

  assign IS_I = (opcode == 7'b0010011);
  assign IS_LW = (funct3 == 3'b010) && (opcode == 7'b0000011);
  assign IS_R = (opcode == 7'b0110011);
  assign IS_SW = (funct3 == 3'b010) && (opcode == 7'b0100011);

endmodule
