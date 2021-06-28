`include "my_or_16.sv"

module my_or_16_test();
  reg [15:0] a, b;
  reg [15:0] expected;
  wire [15:0] out;

  my_or_16 a1(out, a, b);

  task assert_else_error;
    assert (expected == out) else $error("a was %d, b was %d, out was %d but expected %d\n", a, b, out, expected);
  endtask

  initial begin
    a = 16'b0000000000000000; b = 16'b1111111111111111; #10; 
      expected = 16'b1111111111111111; assert_else_error();
    a = 16'b1110000000000000; b = 16'b1010000000000000; #10; 
      expected = 16'b1110000000000000; assert_else_error();
    a = 16'b0000000000001100; b = 16'b1110000000000000; #10; 
      expected = 16'b1110000000001100; assert_else_error();
  end
endmodule
