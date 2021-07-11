`define my_rom_32k 1

module my_rom_32k(out, addr);
  input [14:0] addr;
  output [15:0] out;
  /* verilator lint_off UNDRIVEN */
  reg[15:0] memory[32767:0] /*verilator public*/;
  assign out = memory[addr];  
endmodule