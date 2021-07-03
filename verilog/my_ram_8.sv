`ifndef my_register
  `include "my_register.sv"
`endif
`ifndef my_dmux_8_way
  `include "my_dmux_8_way.sv"
`endif
`ifndef my_mux_8_way
  `include "my_mux_8_way.sv"
`endif

`define my_ram_8 1

module my_ram_8(out, in, addr, clk, load);
  input [15:0] in;
  input [2:0] addr;
  input clk, load;
  output [15:0] out;

  wire a, b, c, d, e, f, g, h;
  my_register reg1(out, in, clk, a);
  my_register reg2(out, in, clk, b);
  my_register reg3(out, in, clk, c);
  my_register reg4(out, in, clk, d);
  my_register reg5(out, in, clk, e);
  my_register reg6(out, in, clk, f);
  my_register reg7(out, in, clk, g);
  my_register reg8(out, in, clk, h);

  wire a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o;
  my_dmux_8_way dmux1(a, b, c, d, e, f, g, h, load, addr);
  my_mux_8_way mux1(out, a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o, addr);
endmodule