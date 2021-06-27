`ifndef my_or
  `include "my_or.sv"
`endif

`ifndef my_and
  `include "my_and.sv"
`endif


module my_xor (o, a, b);
  input a, b;
  output o;
  wire w1, w2;

  my_or or1(w1, a, b);
  nand n1(w2, a, b);
  my_and a1(o, w1, w2);
endmodule