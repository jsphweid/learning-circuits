`ifndef my_full_adder
  `include "my_full_adder.sv"
`endif

module my_adder_16(out, a, b);
  input [15:0] a, b;
  output [15:0] out;
  wire [16:0] last_carry;

  assign last_carry[0] = 0;

  generate
    genvar i;
    for (i = 0; i<=15; i++) begin
      my_full_adder f1(out[i], last_carry[i + 1], a[i], b[i], last_carry[i]);
    end
  endgenerate
endmodule