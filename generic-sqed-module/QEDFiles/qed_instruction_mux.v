`include "qed.vh"

module qed_instruction_mux (/*AUTOARG*/
   // Outputs
   qed_ifu_instruction,
   // Inputs
   ifu_qed_instruction, qed_instruction, //mode,
    ena, exec_dup
   );

   input [31:0] ifu_qed_instruction;
   input [31:0] qed_instruction;
//   input [2:0]  mode;
   input 	exec_dup;
   input        ena;
   
   output [31:0] qed_ifu_instruction;

  // assign padded_qed_instruction = {ifu_qed_instruction[32], qed_instruction[31:0]};
   
   
   // assign qed_ifu_instruction = ena ? ((mode == `ORIGINAL_MODE) ? ifu_qed_instruction :
   //                                     (mode == `DUP_MODE) ? padded_qed_instruction : 
   //                                     32'h0_0100_0000) : 
   //                              ifu_qed_instruction;

   assign qed_ifu_instruction = ena ? ((exec_dup == 1'b0) ? ifu_qed_instruction : qed_instruction) : 
                                ifu_qed_instruction;
   
endmodule // qed_instruction_mux

