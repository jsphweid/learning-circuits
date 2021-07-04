`define my_ram_16k 1

module my_ram_16k(out, in, addr, clk, load);
  input [15:0] in;
  input [13:0] addr;
  input clk, load;
  output [15:0] out;

  reg[15:0] memory[16383:0];
	
  assign out = memory[addr];
	
  always @(posedge clk) begin
    if (load) memory[addr] <= in;
  end
endmodule