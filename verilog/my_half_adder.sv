`ifndef my_xor
  `include "my_xor.sv"
`endif

module my_half_adder(sum, carry, a, b);
  input a, b;
  output sum, carry;

  my_xor x1(sum, a, b);
  my_and a1(carry, a, b);
endmodule