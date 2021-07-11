`ifndef my_register
  `include "my_register.sv"
`endif
`ifndef my_dmux_8_way
  `include "my_dmux_8_way.sv"
`endif
`ifndef my_mux_16_8_way
  `include "my_mux_16_8_way.sv"
`endif
`ifndef my_and
  `include "my_and.sv"
`endif

`define my_ram_8 1

module my_ram_8(out, in, addr, clk, load);
  input [15:0] in;
  input [2:0] addr;
  input clk, load;
  output [15:0] out;

  wire a, b, c, d, e, f, g, h;
  my_dmux_8_way dmux1(a, b, c, d, e, f, g, h, load, addr);

  wire [15:0] a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o;
  my_register reg1(a_o, in, clk, a);
  my_register reg2(b_o, in, clk, b);
  my_register reg3(c_o, in, clk, c);
  my_register reg4(d_o, in, clk, d);
  my_register reg5(e_o, in, clk, e);
  my_register reg6(f_o, in, clk, f);
  my_register reg7(g_o, in, clk, g);
  my_register reg8(h_o, in, clk, h);

  my_mux_16_8_way mux1(out, a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o, addr);
endmodule