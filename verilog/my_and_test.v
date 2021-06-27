module my_and_test;
  reg x, y;
  wire o;

  my_and a1(o, x, y);

  initial begin
    $monitor("my_and_test: At time %2t, x = %d, y = %d, o = %d", $time, x, y, o);
    $dumpfile("vcds/my_and_test.vcd");
    $dumpvars(0, my_and_test);

    x = 0; y = 0; # 10;
    x = 1; y = 0; # 10;
    x = 0; y = 1; # 10;
    x = 1; y = 1; # 10;
    
    $finish;
  end
endmodule
