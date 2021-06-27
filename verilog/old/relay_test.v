module relay_test;
  reg switch, batt;
  wire c;

  our_relay r (c, switch, batt);

  initial begin
    $monitor("relay_test: At time %2t, switch = %d, batt = %d, c = %d", $time, switch, batt, c);
    $dumpfile("vcds/relay_test.vcd");
    $dumpvars(0, relay_test);

    switch = 0; batt = 0; # 10;
    switch = 0; batt = 1; # 10;
    switch = 1; batt = 0; # 10;
    switch = 1; batt = 1; # 10;
    
    $finish;
  end
endmodule
