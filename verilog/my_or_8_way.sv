`ifndef my_or
  `include "my_or.sv"
`endif

module my_or_8_way(out, in);
  input [7:0] in;
  output out;
  wire w1, w2, w3, w4, w5, w6, w7;

  my_or o1(w1, in[0], in[1]);
  my_or o2(w2, w1, in[2]);
  my_or o3(w3, w2, in[3]);
  my_or o4(w4, w3, in[4]);
  my_or o5(w5, w4, in[5]);
  my_or o6(w6, w5, in[6]);
  my_or o7(out, w6, in[7]);

endmodule