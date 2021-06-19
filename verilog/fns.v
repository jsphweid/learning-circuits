// verilog has built in primitives for and/or/not gates...but 
//they are treated like any other module in terms of instantiation

// `module`, module name, ports
module our_nand(o, x, y);
  output o;
  input x, y;
  wire and_wire;

  and a1(and_wire, x, y);
  not n1(o, and_wire);
endmodule
