`include "my_nor.sv"

module my_nor_test();
  reg a;
  reg expected;
  wire out;

  my_nor a1(out, a);

  task assert_else_error;
    assert (expected == out) else $error("a was %d, out was $d but expected %d\n", a, out, expected);
  endtask

  initial begin
    a = 0; #10; expected = 1; assert_else_error();
    a = 1; #10; expected = 0; assert_else_error();
  end

endmodule
