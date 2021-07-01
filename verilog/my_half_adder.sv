`ifndef my_xor
  `include "my_xor.sv"
`endif
`define my_half_adder 1

module my_half_adder(sum, carry, a, b);
  input a, b;
  output sum, carry;

  my_xor x1(sum, a, b);
  my_and a1(carry, a, b);
endmodule