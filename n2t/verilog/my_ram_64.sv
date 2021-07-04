`ifndef my_ram_8
  `include "my_ram_8.sv"
`endif
`ifndef my_mux_16_8_way
  `include "my_mux_16_8_way.sv"
`endif
`ifndef my_dmux_8_way
  `include "my_dmux_8_way.sv"
`endif

`define my_ram_64 1

module my_ram_64(out, in, addr, clk, load);
  input [15:0] in;
  input [5:0] addr;
  input clk, load;
  output [15:0] out;

  
  // load wires for each ram
  wire a, b, c, d, e, f, g, h;
  my_dmux_8_way dmux1(a, b, c, d, e, f, g, h, load, addr[5:3]);

  // 
  wire [15:0] a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o;
  my_ram_8 r1(a_o, in, addr[2:0], clk, a);
  my_ram_8 r2(b_o, in, addr[2:0], clk, b);
  my_ram_8 r3(c_o, in, addr[2:0], clk, c);
  my_ram_8 r4(d_o, in, addr[2:0], clk, d);
  my_ram_8 r5(e_o, in, addr[2:0], clk, e);
  my_ram_8 r6(f_o, in, addr[2:0], clk, f);
  my_ram_8 r7(g_o, in, addr[2:0], clk, g);
  my_ram_8 r8(h_o, in, addr[2:0], clk, h);

  my_mux_16_8_way mux1(out, a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o, addr[5:3]);

endmodule