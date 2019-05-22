module modify_instruction (
// Outputs
qed_instruction,
// Inputs
shamt,
IS_SW,
imm12,
IS_R,
qic_qimux_instruction,
rd,
funct3,
opcode,
rs2,
funct7,
IS_I,
IS_LW,
imm5,
rs1,
imm7);

  input [4:0] shamt;
  input IS_SW;
  input [11:0] imm12;
  input IS_R;
  input [31:0] qic_qimux_instruction;
  input [4:0] rd;
  input [2:0] funct3;
  input [6:0] opcode;
  input [4:0] rs2;
  input [6:0] funct7;
  input IS_I;
  input IS_LW;
  input [4:0] imm5;
  input [4:0] rs1;
  input [6:0] imm7;

  output [31:0] qed_instruction;

  wire [31:0] INS_I;
  wire [31:0] INS_LW;
  wire [31:0] INS_R;
  wire [31:0] INS_SW;
  wire [31:0] INS_CONSTRAINT;

  wire [4:0] NEW_rd;
  wire [4:0] NEW_rs1;
  wire [4:0] NEW_rs2;
  wire [11:0] NEW_imm12;
  wire [6:0] NEW_imm7;

  assign NEW_rd = (rd == 5'b00000) ? rd : {1'b1, rd[3:0]};
  assign NEW_rs1 = (rs1 == 5'b00000) ? rs1 : {1'b1, rs1[3:0]};
  assign NEW_rs2 = (rs2 == 5'b00000) ? rs2 : {1'b1, rs2[3:0]};
  assign NEW_imm12 = {2'b01, imm12[9:0]};
  assign NEW_imm7 = {2'b01, imm7[4:0]};

  assign INS_I = {NEW_imm12, NEW_rs1, funct3, NEW_rd, opcode};
  assign INS_LW = {NEW_imm12, NEW_rs1, funct3, NEW_rd, opcode};
  assign INS_R = {funct7, NEW_rs2, NEW_rs1, funct3, NEW_rd, opcode};
  assign INS_SW = {NEW_imm7, NEW_rs2, NEW_rs1, funct3, imm5, opcode};

  always_comb begin
    if (IS_I) begin
      qed_instruction = INS_I;
    end
    else if (IS_LW) begin
      qed_instruction = INS_LW;
    end
    else if (IS_R) begin
      qed_instruction = INS_R;
    end
    else if (IS_SW) begin
      qed_instruction = INS_SW;
    end
    else begin
      qed_instruction = qic_qimux_instruction;
    end
  end

endmodule
