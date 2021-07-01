`ifndef my_or
  `include "my_or.sv"
`endif
`ifndef my_not
  `include "my_not.sv"
`endif
`ifndef my_and
  `include "my_and.sv"
`endif
`define my_mux 1

module my_mux(o, a, b, sel);
  input a, b, sel;
  output o;

  wire not_wire, w1, w2;

  my_not n1(not_wire, sel);
  my_and a1(w1, not_wire, a);
  my_and a2(w2, sel, b);
  my_or o1(o, w1, w2);
endmodule