`ifndef my_or
  `include "my_or.sv"
`endif
`define my_or_16 1

module my_or_16(out, a, b);
  input [15:0] a, b;
  output [15:0] out;

  generate
    genvar i;
    for (i = 0; i <= 15; i++) begin
      my_or a1(out[i], a[i], b[i]);
    end
  endgenerate

endmodule