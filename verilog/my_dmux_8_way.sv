`ifndef my_dmux_4_way
  `include "my_dmux_4_way.sv"
`endif
`define my_dmux_8_way 1

module my_dmux_8_way(a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out, in, sel);
  input in;
  input [2:0] sel;
  output a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out;

  wire not_msb, top_in, bottom_in;

  my_not n1(not_msb, sel[2]);
  my_and a1(top_in, in, not_msb);
  my_and a2(bottom_in, in, sel[2]);
  my_dmux_4_way d1(a_out, b_out, c_out, d_out, top_in, sel[1:0]);
  my_dmux_4_way d2(e_out, f_out, g_out, h_out, bottom_in, sel[1:0]);

endmodule
