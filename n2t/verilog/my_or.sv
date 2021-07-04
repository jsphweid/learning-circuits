`define my_or 1

module my_or(o, x, y);
  output o;
  input x, y;

  wire w1, w2;

  nand n1(w1, x, x);
  nand n2(w2, y, y);
  nand n3(o, w1, w2);

endmodule