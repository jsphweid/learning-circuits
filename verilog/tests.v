
// test bench
module n_test;
  reg a, b; // inputs for the test
  wire c; // output from our_nand module

  our_nand n (c, a, b);

  // initial blocks are done in parallel
  initial begin

    $monitor("At time %2t, a = %d b = %d c = %d", $time, a, b, c);
    $dumpfile("n.vcd");
    $dumpvars(0, n_test);

    a = 1; b = 0; # 10;
    a = 0; b = 1; # 10;
    a = 1; b = 0; # 10;
    a = 1; b = 1; # 10;

    $finish;
  end
endmodule