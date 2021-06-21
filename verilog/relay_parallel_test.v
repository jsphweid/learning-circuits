module relay_parallel_test;
  reg switch1, switch2, batt1 = 1, batt2 = 1;
  wire c1, c2, c3;
  assign c3 = c1 & c2; // I think this is the correct way to combine two wires

  our_relay r1 (c1, switch1, batt1);
  our_relay r2 (c2, switch2, batt2);

  initial begin
    $monitor("relay_parallel_test: At time %2t, switch1 = %d, switch2 = %d, c3 (single output) = %d", $time, switch1, switch2, c3);
    $dumpfile("vcds/relay_parallel_test.vcd");
    $dumpvars(0, relay_parallel_test);

    switch1 = 0; switch2 = 0; # 10;
    switch1 = 1; switch2 = 0; # 10;
    switch1 = 0; switch2 = 1; # 10;
    switch1 = 1; switch2 = 1; # 10;
    
    $finish;
  end
endmodule
