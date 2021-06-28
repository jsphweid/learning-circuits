`ifndef my_not
  `include "my_not.sv"
`endif

module my_not_16(out, in);
  input [15:0] in;
  output [15:0] out;

  generate
    genvar i;
    for (i = 0; i <=15; i++) begin
      my_not n1(out[i], in[i]);
    end
  endgenerate
endmodule