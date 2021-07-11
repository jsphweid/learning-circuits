`define my_not 1

module my_not(o, a);
  input a;
  output o;

  nand n(o, a, a);
endmodule