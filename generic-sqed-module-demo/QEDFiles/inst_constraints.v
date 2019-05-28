module inst_constraint (
// Inputs
instruction,
clk);

  input [31:0] instruction;
  input clk;

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

  wire FORMAT_I;
  wire ALLOWED_I;
  wire ANDI;
  wire SLTIU;
  wire SRLI;
  wire SLTI;
  wire SRAI;
  wire SLLI;
  wire ORI;
  wire XORI;
  wire ADDI;

  wire FORMAT_LW;
  wire ALLOWED_LW;
  wire LW;

  wire FORMAT_R;
  wire ALLOWED_R;
  wire AND;
  wire SLTU;
  wire MULH;
  wire SRA;
  wire XOR;
  wire SUB;
  wire SLT;
  wire MULHSU;
  wire MULHU;
  wire SRL;
  wire SLL;
  wire ADD;
  wire MUL;
  wire OR;

  wire FORMAT_SW;
  wire ALLOWED_SW;
  wire SW;

  wire ALLOWED_NOP;
  wire NOP;

  assign shamt = instruction[24:20];
  assign imm12 = instruction[31:20];
  assign rd = instruction[11:7];
  assign funct3 = instruction[14:12];
  assign opcode = instruction[6:0];
  assign imm7 = instruction[31:25];
  assign funct7 = instruction[31:25];
  assign imm5 = instruction[11:7];
  assign rs1 = instruction[19:15];
  assign rs2 = instruction[24:20];

  assign FORMAT_I = (rs1 < 16) && (rd < 16);
  assign ANDI = FORMAT_I && (funct3 == 3'b111) && (opcode == 7'b0010011);
  assign SLTIU = FORMAT_I && (funct3 == 3'b011) && (opcode == 7'b0010011);
  assign SRLI = FORMAT_I && (funct3 == 3'b101) && (opcode == 7'b0010011) && (funct7 == 7'b0000000);
  assign SLTI = FORMAT_I && (funct3 == 3'b010) && (opcode == 7'b0010011);
  assign SRAI = FORMAT_I && (funct3 == 3'b101) && (opcode == 7'b0010011) && (funct7 == 7'b0100000);
  assign SLLI = FORMAT_I && (funct3 == 3'b001) && (opcode == 7'b0010011) && (funct7 == 7'b0000000);
  assign ORI = FORMAT_I && (funct3 == 3'b110) && (opcode == 7'b0010011);
  assign XORI = FORMAT_I && (funct3 == 3'b100) && (opcode == 7'b0010011);
  assign ADDI = FORMAT_I && (funct3 == 3'b000) && (opcode == 7'b0010011);
  assign ALLOWED_I = ANDI || SLTIU || SRLI || SLTI || SRAI || SLLI || ORI || XORI || ADDI;

  assign FORMAT_LW = (rs1 < 16) && (rd < 16) && (instruction[31:30] == 00);
  assign LW = FORMAT_LW && (funct3 == 3'b010) && (opcode == 7'b0000011) && (rs1 == 5'b00000);
  assign ALLOWED_LW = LW;

  assign FORMAT_R = (rs2 < 16) && (rs1 < 16) && (rd < 16);
  assign AND = FORMAT_R && (funct3 == 3'b111) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign SLTU = FORMAT_R && (funct3 == 3'b011) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign MULH = FORMAT_R && (funct3 == 3'b001) && (opcode == 7'b0110011) && (funct7 == 7'b0000001);
  assign SRA = FORMAT_R && (funct3 == 3'b101) && (opcode == 7'b0110011) && (funct7 == 7'b0100000);
  assign XOR = FORMAT_R && (funct3 == 3'b100) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign SUB = FORMAT_R && (funct3 == 3'b000) && (opcode == 7'b0110011) && (funct7 == 7'b0100000);
  assign SLT = FORMAT_R && (funct3 == 3'b010) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign MULHSU = FORMAT_R && (funct3 == 3'b010) && (opcode == 7'b0110011) && (funct7 == 7'b0000001);
  assign MULHU = FORMAT_R && (funct3 == 3'b011) && (opcode == 7'b0110011) && (funct7 == 7'b0000001);
  assign SRL = FORMAT_R && (funct3 == 3'b101) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign SLL = FORMAT_R && (funct3 == 3'b001) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign ADD = FORMAT_R && (funct3 == 3'b000) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign MUL = FORMAT_R && (funct3 == 3'b000) && (opcode == 7'b0110011) && (funct7 == 7'b0000001);
  assign OR = FORMAT_R && (funct3 == 3'b110) && (opcode == 7'b0110011) && (funct7 == 7'b0000000);
  assign ALLOWED_R = AND || SLTU || MULH || SRA || XOR || SUB || SLT || MULHSU || MULHU || SRL || SLL || ADD || MUL || OR;

  assign FORMAT_SW = (rs2 < 16) && (rs1 < 16) && (instruction[31:30] == 00);
  assign SW = FORMAT_SW && (funct3 == 3'b010) && (opcode == 7'b0100011) && (rs1 == 5'b00000);
  assign ALLOWED_SW = SW;

  assign NOP = (opcode == 7'b1111111);
  assign ALLOWED_NOP = NOP;

  always @(posedge clk) begin
    assume property (ALLOWED_I || ALLOWED_LW || ALLOWED_R || ALLOWED_SW || ALLOWED_NOP);
  end

endmodule
