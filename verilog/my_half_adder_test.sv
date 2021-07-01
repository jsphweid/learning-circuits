`include "my_half_adder.sv"

module my_half_adder_test;
  reg a, b, sum_expected, carry_expected;
  wire sum, carry;

  my_half_adder a1(sum, carry, a, b);

  task assert_else_error;
    assert (sum == sum_expected && carry == carry_expected) else $error("a was %b, b was %b, expected sum carry to be %b, %b but was %b, %b", a, b, sum_expected, carry_expected, sum, carry);
  endtask

  initial begin
    a = 0; b = 0; #20; sum_expected = 0; carry_expected = 0; assert_else_error();
    a = 0; b = 1; #20; sum_expected = 1; carry_expected = 0; assert_else_error();
    a = 1; b = 0; #20; sum_expected = 1; carry_expected = 0; assert_else_error();
    a = 1; b = 1; #20; sum_expected = 0; carry_expected = 1; assert_else_error();
  end
endmodule