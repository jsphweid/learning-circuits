module latch_test;
  reg set, reset;
  wire o1;

  latch l1(o1, set, reset);

  initial begin
    $monitor("latch_test: At time %2t, set = %b, reset = %b, o1 = %b", $time, set, reset, o1);
    $dumpfile("vcds/latch_test.vcd");
    $dumpvars(0, latch_test);

    set = 0; reset = 0; # 10;
    set = 1; reset = 0; # 10;
    set = 0; reset = 0; # 10;
    set = 0; reset = 1; # 10;
    set = 0; reset = 0; # 10;
    
    $finish;
  end
endmodule
