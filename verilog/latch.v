module latch(o, set, reset);
  output o;
  input set, reset;

  wire or_output, and_output, not_output;

  or o1(or_output, set, and_output);
  not n1(not_output, reset);
  and a1(and_output, or_output, not_output);
  assign o = and_output;

endmodule
