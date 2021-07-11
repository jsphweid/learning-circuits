`ifndef my_1_bit_register
  `include "my_1_bit_register.sv"
`endif

`define my_register 1

module my_register(out, in, clk, load);
  input [15:0] in;
  input load, clk;
  output [15:0] out;

  generate
    genvar i;
    for (i = 0; i <=15; i++) begin
      my_1_bit_register m1(out[i], in[i], clk, load);
    end
  endgenerate


endmodule