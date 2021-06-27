module my_and(o, x, y);
  output o;
  input x, y;

  wire w1, w2;

  nand n1(w1, x, y);
  nand n2(w2, x, y);
  nand n3(o, w1, w2);

endmodule