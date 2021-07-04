`include "my_not_16.sv"

module my_not_16_test();
  reg [15:0] in;
  reg [15:0] expected;
  wire [15:0] out;

  my_not_16 a1(out, in);

  task assert_else_error;
    assert (expected == out) else $error("in was %b, out was %b but expected %b\n", in, out, expected);
  endtask

  initial begin
    in = 16'b0000000000000000; #10; expected = 16'b1111111111111111; assert_else_error();
    in = 16'b1111111111111111; #10; expected = 16'b0000000000000000; assert_else_error();
    in = 16'b1111100011111100; #10; expected = 16'b0000011100000011; assert_else_error();
  end
endmodule
