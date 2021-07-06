`define my_screen 1

module my_screen(out, in, addr, clk, load);
  input [15:0] in;
  input [12:0] addr;
  input clk, load;
  output [15:0] out;

  reg[15:0] memory[8191:0] /*verilator public*/;
	
  assign out = memory[addr];
	
  always @(posedge clk) begin
    if (load) memory[addr] <= in;
  end
endmodule