`include "my_or.sv"

module my_or_test();
  reg a, b;
  reg expected;
  wire out;

  my_or a1(out, a, b);

  task assert_else_error;
    assert (expected == out) else $error("a was %d, b was %d, out was %d but expected %d\n", a, b, out, expected);
  endtask

  initial begin
    a = 0; b = 0; #10; expected = 0; assert_else_error();
    a = 1; b = 0; #10; expected = 1; assert_else_error();
    a = 0; b = 1; #10; expected = 1; assert_else_error();
    a = 1; b = 1; #10; expected = 1; assert_else_error();
  end

endmodule
