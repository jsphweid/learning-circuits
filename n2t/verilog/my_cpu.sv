`ifndef my_or
  `include "my_or.sv"
`endif
`ifndef my_mux_16
  `include "my_mux_16.sv"
`endif
`ifndef my_not
  `include "my_not.sv"
`endif
`ifndef my_register
  `include "my_register.sv"
`endif
`ifndef my_alu
  `include "my_alu.sv"
`endif
`ifndef my_pc
  `include "my_pc.sv"
`endif
`define my_cpu 1

module my_cpu(outM, writeM, addressM, pc, inM, instruction, clk, reset);
  input [15:0] inM, instruction;
  input reset, clk;
  output [15:0] outM;
  output writeM;
  output [14:0] addressM, pc;

  // inM = M value input... M is the value at RAM[A]

  // Writing to memory...
  //    outM -> value we need to write to M register (affected instantaneously by instruction)
  //    writeM -> 1 (affected instantaneously by instruction)
  //    addressM -> memory address it should be stored (clocked, commit values on next clock cycle)
  wire is_c_instruction, is_a_instruction;
  assign is_c_instruction = instruction[15];
  my_not not_msb(is_a_instruction, instruction[15]);

  //////////////////////////////    ALU    //////////////////////////////////
  // module my_alu(out, zr, ng, x, y, zx, nx, zy, ny, f, no);
  wire [15:0] alu_out;
  wire zr, ng;
  // 6 control bits, I bet they line up with the instruction in some way....
  // just need to figure out what the x,y are. Clearly one is D and the other
  // is A/M depending on the value of one bit
  wire [15:0] a_or_m;
  my_mux_16 get_2nd_input(a_or_m, reg_a_out, inM, instruction[12]);
  my_alu alu1(alu_out, zr, ng, reg_d_out, a_or_m, instruction[11], instruction[10], instruction[9], instruction[8], instruction[7], instruction[6]);


  ////////////////////////////// M OUTPUT  //////////////////////////////////
  // It should writeM when:
  //  * instruction is C instruction
  //  * destination bit enabled instruction[3]
  my_and writeM_enabled(writeM, is_c_instruction, instruction[3]);
  // What should it write M... the ALU output, right?
  assign outM = alu_out;

  //////////////////////////////     PC     /////////////////////////////////
  // If reset is enabled, it should return the pc to 0 (on the next clock tick?)
  // increment - Whether we should increment - always increment since reset/load have priority
  // load - 1 if there is a jump
  // in - always the address in A register. It won't jump unless load is 1
  wire lessThan = ng;
  wire zero = zr;
  wire greaterThan = !(zero || lessThan);
  wire jump = is_c_instruction && (instruction[0] && greaterThan) || (instruction[1] && zero) || (instruction[2] && lessThan);
  wire [15:0] pc_out_temp;
  wire notJump = !jump;

  my_pc pc1(pc_out_temp, reg_a_out, jump, notJump, reset, not_clk);
  assign pc = pc_out_temp[14:0];

  ////////////////////////////// REGISTERS //////////////////////////////////
  // module my_register(out, in, clk, load);
  
  // Whether or not to write to register A is determined by the type of instruction
  //  if the first bit is a 0, then it is a write to A
  // NOTE: we'll store the entire A instruction, although the address is only [14:0]. This
  //  is because my_register expects a [15:0]
  // Whether to load it depends on:
  //  * is a A instruction
  //  * d1 (destination in the C-Instruction) (`instruction[5]`)
  // The input can be several things:
  //  * is the instruction itself (since it contains an address for A instructions)
  //  * output of some ALU operation
  // If it's an A instruction, it'll store the address, if it's a C instructionwire not_clock;
  
  my_not clock_not(not_clk, clk);

  wire [15:0] reg_a_out, reg_d_out, mux_a_out;
  wire is_load_from_c_instruction;
  my_and special_c(is_load_from_c_instruction, is_c_instruction, instruction[5]);
  my_or load_a_condition(should_load_a_reg, is_a_instruction, is_load_from_c_instruction);
  my_mux_16 mux_a(mux_a_out, instruction, alu_out, is_load_from_c_instruction);
  my_register regA(reg_a_out, mux_a_out, not_clk, should_load_a_reg);
  assign addressM = reg_a_out[14:0];
  
  // The input here is the output of some ALU operation
  // Whether to load it depends on:
  //  * is a C instruction
  //  * d2 (destination in the C-Instruction) (`instruction[4]`)
  wire should_load_d_reg;
  my_and load_d_condition(should_load_d_reg, is_c_instruction, instruction[4]);
  my_register regD(reg_d_out, alu_out, clk, should_load_d_reg);

endmodule