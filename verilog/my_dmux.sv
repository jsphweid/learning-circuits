`ifndef my_not
  `include "my_not.sv"
`endif

`ifndef my_and
  `include "my_and.sv"
`endif

module my_dmux(a_out, b_out, in, sel);
  input in, sel;
  output a_out, b_out;

  wire not_sel;
  
  my_not n1(not_sel, sel);
  my_and a1(a_out, not_sel, in);
  my_and a2(b_out, sel, in);
endmodule