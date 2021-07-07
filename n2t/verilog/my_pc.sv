`ifndef my_incrementer_16
  `include "my_incrementer_16.sv"
`endif
`ifndef my_register
  `include "my_register.sv"
`endif
`ifndef my_mux_16_4_way
  `include "my_mux_16_4_way.sv"
`endif
`define my_pc 1

module my_pc(out, in, load, inc, reset, clk);
  input [15:0] in;
  input load, inc, reset, clk;
  output [15:0] out;

  wire [15:0] next_inc;
  my_incrementer_16 next(next_inc, out);
  wire [15:0] mux_out;
  wire [1:0] sel;

  // This feels like cheating... but it works...
  assign sel = reset ? 2'b11 : load ? 2'b01 : inc ? 2'b10 : 2'b00;
  wire ld = !(sel == 2'b00);
  
  my_mux_16_4_way mux(mux_out, out, in, next_inc, 16'b0, sel);
  my_register reg1(out, mux_out, clk, ld);
endmodule