`ifndef my_adder_16
  `include "my_adder_16.sv"
`endif
`ifndef my_not_16
  `include "my_not_16.sv"
`endif
`ifndef my_or_16
  `include "my_or_16.sv"
`endif

`define my_incrementer_16 1

module my_incrementer_16(out, a);
  input [15:0] a;
  output [15:0] out;

  wire [15:0] a_inverted, ones, combined;
  my_not_16 n1(a_inverted, a);
  my_or_16 o1(ones, a_inverted, a);
  my_adder_16 add1(combined, ones, a_inverted);
  my_not_16 n2(out, combined);
endmodule