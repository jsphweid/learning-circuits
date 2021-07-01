module nor_latch_test;
  reg set, reset;
  wire o1, o2;

  nor_latch l1(o1, o2, set, reset);

  initial begin
    $monitor("nor_latch_test: At time %2t, set = %b, reset = %b, o1 = %b, o2 = %b", $time, set, reset, o1, o2);
    $dumpfile("vcds/nor_latch_test.vcd");
    $dumpvars(0, nor_latch_test);

    set = 0; reset = 0; # 10;
    set = 1; reset = 0; # 10;
    set = 0; reset = 0; # 10;
    set = 0; reset = 1; # 10;
    set = 0; reset = 0; # 10;
    
    $finish;
  end
endmodule
