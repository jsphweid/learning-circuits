`ifndef my_and
  `include "my_and.sv"
`endif
`define my_and_16 1

module my_and_16(out, a, b);
  input [15:0] a, b;
  output [15:0] out;

  generate
    genvar i;
    for (i = 0; i <= 15; i++) begin
      my_and a1(out[i], a[i], b[i]);
    end
  endgenerate

endmodule