`ifndef my_half_adder
  `include "my_half_adder.sv"
`endif
`define my_full_adder 1

module my_full_adder(sum, carry, a, b, c);
  input a, b, c;
  output sum, carry;

  wire half_adder_sum, half_adder_carry, w1;

  my_half_adder h1(half_adder_sum, half_adder_carry, a, b);
  my_xor x1(sum, half_adder_sum, c);
  my_and a1(w1, half_adder_sum, c);
  my_or o1(carry, w1, half_adder_carry);
endmodule
