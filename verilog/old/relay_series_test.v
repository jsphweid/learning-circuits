module relay_series_test;
  reg switch1, switch2, batt1 = 1;
  wire c1, c2;

  our_relay r1 (c1, switch1, batt1);
  our_relay r2 (c2, switch2, c1); // output of the first (c1) controls the battery of the second

  initial begin
    $monitor("relay_series_test: At time %2t, switch1 = %b, c2 (2nd relay) = %b", $time, switch1, c2);
    $dumpfile("vcds/relay_series_test.vcd");
    $dumpvars(0, relay_series_test);

    switch1 = 0; switch2 = 0; # 10;
    switch1 = 1; switch2 = 0; # 10;
    switch1 = 0; switch2 = 1; # 10;
    switch1 = 1; switch2 = 1; # 10;
    
    $finish;
  end
endmodule
