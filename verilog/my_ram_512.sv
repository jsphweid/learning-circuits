`ifndef my_ram_64
  `include "my_ram_64.sv"
`endif
`ifndef my_mux_16_8_way
  `include "my_mux_16_8_way.sv"
`endif
`ifndef my_dmux_8_way
  `include "my_dmux_8_way.sv"
`endif

`define my_ram_512 1

module my_ram_512(out, in, addr, clk, load);
  input [15:0] in;
  input [8:0] addr;
  input clk, load;
  output [15:0] out;

  reg[15:0] memory[511:0];
	
  assign out = memory[addr];
	
  always @(posedge clk) begin
    if (load) memory[addr] <= in;
  end


  // NOTE: below is my implementation. I stopped here at this point because
  // hand-rolling everything becomes really slow -- might as well use the built-in
  // versions now that we know roughly how everything works anyways
  
  // wire a, b, c, d, e, f, g, h;
  // my_dmux_8_way dmux1(a, b, c, d, e, f, g, h, load, addr[8:6]);

  // wire [15:0] a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o;
  // my_ram_64 r1(a_o, in, addr[5:0], clk, a);
  // my_ram_64 r2(b_o, in, addr[5:0], clk, b);
  // my_ram_64 r3(c_o, in, addr[5:0], clk, c);
  // my_ram_64 r4(d_o, in, addr[5:0], clk, d);
  // my_ram_64 r5(e_o, in, addr[5:0], clk, e);
  // my_ram_64 r6(f_o, in, addr[5:0], clk, f);
  // my_ram_64 r7(g_o, in, addr[5:0], clk, g);
  // my_ram_64 r8(h_o, in, addr[5:0], clk, h);

  // my_mux_16_8_way mux1(out, a_o, b_o, c_o, d_o, e_o, f_o, g_o, h_o, addr[8:6]);
endmodule