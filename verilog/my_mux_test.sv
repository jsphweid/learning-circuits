`include "my_mux.sv"

module my_mux_test();
  reg a, b, sel, expected;
  wire out;

  my_mux a1(out, a, b, sel);

  task assert_else_error;
    assert (expected == out) else $error("a was %d, b was %d, sel was %d, out was %d but expected %d\n", a, b, sel, out, expected);
  endtask

  initial begin
    a = 0; b = 0; sel = 0; #10; expected = 0; assert_else_error();
    a = 0; b = 1; sel = 0; #10; expected = 0; assert_else_error();
    a = 1; b = 0; sel = 0; #10; expected = 1; assert_else_error();
    a = 1; b = 1; sel = 0; #10; expected = 1; assert_else_error();
    a = 0; b = 0; sel = 1; #10; expected = 0; assert_else_error();
    a = 0; b = 1; sel = 1; #10; expected = 1; assert_else_error();
    a = 1; b = 0; sel = 1; #10; expected = 0; assert_else_error();
    a = 1; b = 1; sel = 1; #10; expected = 1; assert_else_error();
  end

endmodule
