`include "my_1_bit_register.sv"

module my_1_bit_register_test;
  reg in, clk, load, expected_out;
  wire out;

  my_1_bit_register b1(out, in, clk, load);

  task assert_else_error(expected_out);
    assert (out == expected_out) else $error("in was %b, clk was %b, load was %b, out was %b but expected %b", in, clk, load, out, expected_out);
  endtask

  initial begin
    #1; in = 0; load = 1; clk = 0;
    #1; in = 0; load = 1; clk = 1; #1; assert_else_error(0);
    #1; in = 1; load = 0; clk = 0; #1; assert_else_error(0);
    #1; in = 1; load = 0; clk = 1; #1; assert_else_error(0);
    #1; in = 1; load = 1; clk = 0; #1; assert_else_error(0);
    #1; in = 1; load = 1; clk = 1; #1; assert_else_error(1);
    #1; in = 0; load = 1; clk = 0; #1; assert_else_error(1);
    #1; in = 0; load = 1; clk = 1; #1; assert_else_error(0);
    #1; in = 0; load = 0; clk = 0; #1; assert_else_error(0);
    #1; in = 0; load = 0; clk = 1; #1; assert_else_error(0);
    #1; in = 1; load = 0; clk = 0; #1; assert_else_error(0);
    #1; in = 1; load = 0; clk = 1; #1; assert_else_error(0);
    #1; in = 0; load = 1; clk = 0; #1; assert_else_error(0);
    #1; in = 0; load = 1; clk = 1; #1; assert_else_error(0);
    #1; in = 1; load = 1; clk = 0; #1; assert_else_error(0);
    #1; in = 1; load = 1; clk = 1; #1; assert_else_error(1);
  end
endmodule