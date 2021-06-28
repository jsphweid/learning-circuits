`ifndef my_not
  `include "my_not.sv"
`endif

`ifndef my_and
  `include "my_and.sv"
`endif

module my_dmux_4_way(a_out, b_out, c_out, d_out, in, sel);
  input in;
  input [1:0] sel;
  output a_out, b_out, c_out, d_out;
  wire not_msb, not_lsb, t1, t2, t3, t4;

  my_not n1(not_msb, sel[1]);
  my_not n2(not_lsb, sel[0]);
  my_and a1(t1, not_msb, not_lsb);
  my_and a2(t2, not_msb, sel[0]);
  my_and a3(t3, not_lsb, sel[1]);
  my_and a4(t4, sel[0], sel[1]);
  
  my_and a5(a_out, in, t1);
  my_and a6(b_out, in, t2);
  my_and a7(c_out, in, t3);
  my_and a8(d_out, in, t4);
  
endmodule