module qed (
// Outputs
vld_out,
qed_ifu_instruction,
// Inputs
ena,
ifu_qed_instruction,
clk,
exec_dup,
stall_IF,
rst);

  input ena;
  input [31:0] ifu_qed_instruction;
  input clk;
  input exec_dup;
  input stall_IF;
  input rst;

  output vld_out;
  output [31:0] qed_ifu_instruction;
  wire [4:0] shamt;
  wire [11:0] imm12;
  wire [4:0] rd;
  wire [2:0] funct3;
  wire [6:0] opcode;
  wire [6:0] imm7;
  wire [6:0] funct7;
  wire [4:0] imm5;
  wire [4:0] rs1;
  wire [4:0] rs2;

  wire IS_I;
  wire IS_LW;
  wire IS_R;
  wire IS_SW;

  wire [31:0] qed_instruction;
  wire [31:0] qic_qimux_instruction;

  qed_decoder dec (.ifu_qed_instruction(qic_qimux_instruction),
                   .shamt(shamt),
                   .imm12(imm12),
                   .rd(rd),
                   .funct3(funct3),
                   .opcode(opcode),
                   .imm7(imm7),
                   .funct7(funct7),
                   .imm5(imm5),
                   .rs1(rs1),
                   .rs2(rs2),
                   .IS_I(IS_I),
                   .IS_LW(IS_LW),
                   .IS_R(IS_R),
                   .IS_SW(IS_SW));

  modify_instruction minst (.qed_instruction(qed_instruction),
                            .qic_qimux_instruction(qic_qimux_instruction),
                            .shamt(shamt),
                            .imm12(imm12),
                            .rd(rd),
                            .funct3(funct3),
                            .opcode(opcode),
                            .imm7(imm7),
                            .funct7(funct7),
                            .imm5(imm5),
                            .rs1(rs1),
                            .rs2(rs2),
                            .IS_I(IS_I),
                            .IS_LW(IS_LW),
                            .IS_R(IS_R),
                            .IS_SW(IS_SW));

  qed_instruction_mux imux (.qed_ifu_instruction(qed_ifu_instruction),
                            .ifu_qed_instruction(ifu_qed_instruction),
                            .qed_instruction(qed_instruction),
                            .exec_dup(exec_dup),
                            .ena(ena));

  qed_i_cache qic (.qic_qimux_instruction(qic_qimux_instruction),
                   .vld_out(vld_out),
                   .clk(clk),
                   .rst(rst),
                   .exec_dup(exec_dup),
                   .IF_stall(stall_IF),
                   .ifu_qed_instruction(ifu_qed_instruction));

endmodule
