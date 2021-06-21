module two_relay_test;
  reg switch1, batt1 = 1, batt2 = 1;
  wire c1, c2;

  our_relay r1 (c1, switch1, batt1);
  our_relay r2 (c2, c1, batt2); // output of the first (c1) controls the switch of the second

  initial begin
    $monitor("two_relay_test: At time %2t, switch1 = %d, c2 (2nd relay) = %d", $time, switch1, c2);
    $dumpfile("vcds/two_relay_test.vcd");
    $dumpvars(0, two_relay_test);

    switch1 = 0; # 10;
    switch1 = 1; # 10;
    switch1 = 0; # 10;
    switch1 = 1; # 10;
    
    $finish;
  end
endmodule
