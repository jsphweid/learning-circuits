`include "my_dmux.sv"

module my_dmux_test();
  reg in, sel, a_expected, b_expected;
  wire a_out, b_out;

  my_dmux a1(a_out, b_out, in, sel);

  task assert_else_error;
    assert (a_expected == a_out && b_expected == b_out) else $error("in was %d, select was %d, a_out was %d, b_out was %d but expected a_out to be %d and b_out to be %d\n", in, sel, a_out, b_out, a_expected, b_expected);
  endtask

  initial begin
    in = 0; sel = 0; #10; a_expected = 0; b_expected = 0; assert_else_error();
    in = 1; sel = 0; #10; a_expected = 1; b_expected = 0; assert_else_error();
    in = 0; sel = 1; #10; a_expected = 0; b_expected = 0; assert_else_error();
    in = 1; sel = 1; #10; a_expected = 0; b_expected = 1; assert_else_error();
  end
endmodule
