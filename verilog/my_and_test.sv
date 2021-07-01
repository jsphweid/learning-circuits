`include "my_and.sv"

module my_and_test();
  reg a, b;
  reg expected;
  wire out;

  my_and a1(out, a, b);

  task assert_else_error;
    assert (expected == out) else $error("a was %b, b was %b, out was %b but expected %b\n", a, b, out, expected);
  endtask

  initial begin
    a = 0; b = 0; #10; expected = 0; assert_else_error();
    a = 1; b = 0; #10; expected = 0; assert_else_error();
    a = 0; b = 1; #10; expected = 0; assert_else_error();
    a = 1; b = 1; #10; expected = 1; assert_else_error();
  end

endmodule
