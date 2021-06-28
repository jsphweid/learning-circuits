`include "my_dmux_4_way.sv"

module my_dmux_4_way_test;
  reg in, a_expected, b_expected, c_expected, d_expected;
  reg [1:0] sel;
  wire a_out, b_out, c_out, d_out;

  my_dmux_4_way a1(a_out, b_out, c_out, d_out, in, sel);

  task assert_else_error;
    assert (a_expected == a_out && b_expected == b_out && c_expected == c_out && d_expected == d_out) 
      else $error("in was %d, sel was %d, but output was not correct", in, sel);
  endtask

  initial begin
    in = 0; sel = 2'b00; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; assert_else_error();
    in = 1; sel = 2'b00; #10; a_expected = 1; b_expected = 0; c_expected = 0; d_expected = 0; assert_else_error();
    in = 0; sel = 2'b01; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; assert_else_error();
    in = 1; sel = 2'b01; #10; a_expected = 0; b_expected = 1; c_expected = 0; d_expected = 0; assert_else_error();
    in = 0; sel = 2'b10; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; assert_else_error();
    in = 1; sel = 2'b10; #10; a_expected = 0; b_expected = 0; c_expected = 1; d_expected = 0; assert_else_error();
    in = 0; sel = 2'b11; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; assert_else_error();
    in = 1; sel = 2'b11; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 1; assert_else_error();
  end
endmodule