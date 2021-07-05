`define my_rom_32k 1

module my_rom_32k(out, addr);
  input [14:0] addr;
  output [15:0] out;
  reg[14:0] memory[32767:0];
  assign out = memory[addr];
endmodule