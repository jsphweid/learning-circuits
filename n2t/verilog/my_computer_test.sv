`include "my_computer.sv"

module my_computer_test();
  reg reset, clk;

  my_computer c1(reset, clk);

  task assert_else_error(reg[15:0] expected_instruction);
    assert (expected_instruction==c1.rom_out_instruction) else $error("instruction was %b but expected %b", c1.rom_out_instruction, expected_instruction);
  endtask

  initial begin

  // fill rom
  c1.rom.memory[0] = 16'b0001111111100000;
  c1.rom.memory[1] = 16'b1110110000010000;
  c1.rom.memory[2] = 16'b0000000000010000;
  c1.rom.memory[3] = 16'b1110001100001000;
  c1.rom.memory[4] = 16'b0000000000010001;
  c1.rom.memory[5] = 16'b1110101010001000;
  c1.rom.memory[6] = 16'b0000000000010000;
  c1.rom.memory[7] = 16'b1111110000010000;

  #1;
  
  reset = 1; clk = 0; #1; clk = 1; #1;
  reset = 0; 
  
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b0001111111100000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b1110110000010000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b0000000000010000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b1110001100001000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b0000000000010001);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b1110101010001000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b0000000000010000);
  clk = 0; #1; clk = 1; #1; assert_else_error(16'b1111110000010000);
  end
endmodule
