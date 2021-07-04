`include "my_register.sv"

module my_register_test;
  reg [15:0] in, expected_out;
  reg clk, load;
  wire [15:0] out;

  my_register reg1(out, in, clk, load);
  
  task assert_else_error(reg [15:0] exp);
    assert (out == exp) else $error("in: %b, load: %b, clk: %b, out: %b but expected %b", in, load, clk, out, exp);
  endtask

  initial begin
    // initialize to 0
    #1; clk = 0; #1; in = 0; load = 0;
    #1; clk = 1; #1; assert_else_error(0);
    #1; clk = 0; #1; in = 0; load = 1; #1; assert_else_error(0);
    
    // load is 1, clk turns 1, but in is 0, so it is set/stays at 0
    #1; clk = 1; #1; assert_else_error(0);

    // stays off because clk/load are 0
    #1; clk = 0; #1; in = -32123; load = 0; #1; assert_else_error(0);
    #1; clk = 1; #1; assert_else_error(0);
    #1; clk = 0; #1; in = 11111; load = 0; #1; assert_else_error(0);
    #1; clk = 1; #1; assert_else_error(0);
    #1; clk = 0; #1; in = -32123; load = 1; #1; assert_else_error(0);
    
    // finally changes because load is set, in is set, and clk becomes non-zero
    #1; clk = 1; #1; assert_else_error(-32123);
    #1; clk = 0; #1; assert_else_error(-32123);

    // conditions are good for change, but input is still the same
    #1; clk = 1; #1; assert_else_error(-32123);

    // load/clk not lined up so can't change
    #1; clk = 0; #1; in = -32123; load = 0; #1; assert_else_error(-32123);
    #1; clk = 1; #1; assert_else_error(-32123);
    #1; clk = 0; #1; in = 12345; load = 1; #1; assert_else_error(-32123);
    
    // load/clk finally lined up with a different in value
    #1; clk = 1; #1; assert_else_error(12345);
    
    // stays because load/clk isn't 1
    #1; clk = 0; #1; in = 0; load = 0; #1; assert_else_error(12345);
    #1; clk = 1; #1; clk = 0; #1; assert_else_error(12345);
    #1; in = 0; load = 1; #1; assert_else_error(12345);

    // everything can finally change because load/clk on same page and input is different
    #1; clk = 1; #1; assert_else_error(0);

    // again, remains because load/clk aren't both 1
    #1; clk = 0; #1; in = 1; load = 0; #1; assert_else_error(0);
    #1; clk = 1; #1; assert_else_error(0);
    #1; clk = 0; #1; in = 1; load = 1; #1; assert_else_error(0);
    
    // load/clk finally both 1
    #1; clk = 1; #1; assert_else_error(1);
  end
endmodule