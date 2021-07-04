`define my_ram_4k 1

module my_ram_4k(out, in, addr, clk, load);
  input [15:0] in;
  input [11:0] addr;
  input clk, load;
  output [15:0] out;

  reg[15:0] memory[4095:0];
	
  assign out = memory[addr];
	
  always @(posedge clk) begin
    if (load) memory[addr] <= in;
  end
endmodule