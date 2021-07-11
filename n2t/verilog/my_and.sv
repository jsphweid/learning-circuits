`define my_and 1

module my_and(o, x, y);
  output o;
  input x, y;
  assign o = x && y;
endmodule