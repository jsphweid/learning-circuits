`ifndef my_ram_16k
  `include "my_ram_16k.sv"
`endif
`ifndef my_mux_16
  `include "my_mux_16.sv"
`endif
`include "my_screen.sv"
`define my_memory 1

module my_memory(out, in, addr, clk, load);
  input [15:0] in;
  input [14:0] addr;
  input clk, load;
  output [15:0] out;

  wire[15:0] outM, outS, outSK;
  wire N14, Mload, Sload;
	
  my_not g1(N14, addr[14]);
  my_and g2(Mload, N14, load);
  my_and g3(Sload, addr[14], load);
  
  my_ram_16k ram16k(outM, in, addr[13:0], clk, Mload);
  my_screen screen(outS, in, addr[12:0], clk, Sload);
  reg [15:0] scancode /*verilator public*/;

  // integer f;
  // always @(clk) begin
  //   f = $fopen("output2.txt","a");
  //   $fwrite(f,"my_memory: clk %b, in %b, addr %b, scancode %b, out %b, load %b, outSK %b, outM %b, outS %b\n", clk, in, addr, scancode, out, load, outSK, outM, outS);
  //   $fclose(f);
  // end
  
  my_mux_16 g4(out, outM, outSK, addr[14]);
  my_mux_16 g5(outSK, outS, scancode,  addr[13]);
endmodule
