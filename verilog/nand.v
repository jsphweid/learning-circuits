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


module nand_test;
  reg a, b; // inputs for the test
  wire c; // output from our_nand module

  our_nand n (c, a, b);

  // initial blocks are done in parallel
  initial begin

    $monitor("nand test: At time %2t, a = %d b = %d c = %d", $time, a, b, c);
    $dumpfile("vcds/nand.vcd");
    $dumpvars(0, nand_test);

    a = 1; b = 0; # 10;
    a = 0; b = 1; # 10;
    a = 1; b = 0; # 10;
    a = 1; b = 1; # 10;

    $finish;
  end
endmodule