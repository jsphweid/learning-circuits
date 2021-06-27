module my_nor(o, a);
  input a;
  output o;

  nand(o, a, a);
endmodule