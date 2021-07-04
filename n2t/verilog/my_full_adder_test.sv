`include "my_full_adder.sv"

module my_full_adder_test;
  reg a, b, c, sum_expected, carry_expected;
  wire sum, carry;

  my_full_adder a1(sum, carry, a, b, c);

  task assert_else_error;
    assert (sum == sum_expected && carry == carry_expected) else $error("a was %b, b was %b, c was %b... expected sum/carry to be %b/%b, but was %b/%b", a, b, c, sum_expected, carry_expected, sum, carry);
  endtask

  initial begin
    a = 0; b = 0; c = 0; #10; sum_expected = 0; carry_expected = 0; assert_else_error();
    a = 0; b = 0; c = 1; #10; sum_expected = 1; carry_expected = 0; assert_else_error();
    a = 0; b = 1; c = 0; #10; sum_expected = 1; carry_expected = 0; assert_else_error();
    a = 0; b = 1; c = 1; #10; sum_expected = 0; carry_expected = 1; assert_else_error();
    a = 1; b = 0; c = 0; #10; sum_expected = 1; carry_expected = 0; assert_else_error();
    a = 1; b = 0; c = 1; #10; sum_expected = 0; carry_expected = 1; assert_else_error();
    a = 1; b = 1; c = 0; #10; sum_expected = 0; carry_expected = 1; assert_else_error();
    a = 1; b = 1; c = 1; #10; sum_expected = 1; carry_expected = 1; assert_else_error();
  end

endmodule
