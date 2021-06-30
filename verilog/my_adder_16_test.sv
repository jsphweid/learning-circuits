`include "my_adder_16.sv"

module my_adder_16_test;
  reg [15:0] a, b, expected;
  wire [15:0] out;
  
  my_adder_16 a1(out, a, b);

  task assert_else_error;
    assert (expected == out) else $error("a was %d, b was %d, out was %d but expected %d", a, b, out, expected);
  endtask

  initial begin
    a = 16'b0000000000000000; b = 16'b0000000000000000; #10; expected = 16'b0000000000000000; assert_else_error();
    a = 16'b0000000000000001; b = 16'b0000000000000000; #10; expected = 16'b0000000000000001; assert_else_error();
    a = 16'b0000000000000001; b = 16'b0000000000000001; #10; expected = 16'b0000000000000010; assert_else_error();
    a = 16'b0000000000001111; b = 16'b0000000000001111; #10; expected = 16'b0000000000011110; assert_else_error();
    a = 16'b0100000000000000; b = 16'b0100000000000000; #10; expected = 16'b1000000000000000; assert_else_error();
    
    // TODO: verify these overflow cases... in the book it says "overflow is neither detected or handled"
    a = 16'b1000000000000000; b = 16'b1000000000000000; #10; expected = 16'b0000000000000000; assert_else_error();
  end
endmodule