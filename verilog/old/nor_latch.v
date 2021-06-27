module nor_latch(o1, o2, set, reset);
  input set, reset;
  output o1, o2;

  nor n1(o1, set, o2);
  nor n2(o2, o1, reset);
endmodule

