`ifndef my_mux_16_4_way
  `include "my_mux_16_4_way.sv"
`endif
`define my_mux_16_8_way 1

module my_mux_16_8_way(out, a, b, c, d, e, f, g, h, sel);
  input [15:0] a, b, c, d, e, f, g, h;
  input [2:0] sel;
  output [15:0] out;

  wire [15:0] w1, w2;

  // NOTE: see "my_mux_16_4_way.sv" for note about alternate solution
  my_mux_16_4_way m1(w1, a, b, c, d, sel[1:0]);
  my_mux_16_4_way m2(w2, e, f, g, h, sel[1:0]);
  my_mux_16 m3(out, w1, w2, sel[2]);

endmodule