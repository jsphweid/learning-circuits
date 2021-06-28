`include "my_or_8_way.sv"

module my_or_8_way_test;
  reg [7:0] in;
  reg expected;
  wire out;

  my_or_8_way a1(out, in);

  task assert_else_error;
    assert (expected == out) else $error("in was %d and out was %d but expected %d", in, out, expected);
  endtask

  initial begin
    in = 8'b00000000; #10; expected = 0; assert_else_error();
    in = 8'b00000010; #10; expected = 1; assert_else_error();
    in = 8'b00010111; #10; expected = 1; assert_else_error();
    in = 8'b11111111; #10; expected = 1; assert_else_error();
  end
endmodule