`include "my_dff.sv"

module my_dff_test;
  reg clk, data, expected_out;
  wire out;

  my_dff d1(out, data, clk);

  task assert_else_error;
    assert (out == expected_out) else $error("data was %b, clk was %b, out was %b but expected %b", data, clk, out, expected_out);
  endtask

  initial begin
    data = 0; clk = 0; #1;
    data = 0; clk = 1; expected_out = 0; #1; assert_else_error(); #1;
    data = 1; clk = 0; expected_out = 0; #1; assert_else_error(); #1;
    data = 1; clk = 1; expected_out = 1; #1; assert_else_error(); #1;
    data = 0; clk = 0; expected_out = 1; #1; assert_else_error(); #1;
    data = 0; clk = 1; expected_out = 0; #1; assert_else_error(); #1;
    data = 1; clk = 0; expected_out = 0; #1; assert_else_error(); #1;
    data = 1; clk = 1; expected_out = 1; #1; assert_else_error(); #1;
  end
endmodule