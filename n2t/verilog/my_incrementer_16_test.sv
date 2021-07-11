`include "my_incrementer_16.sv"

module my_incrementer_16_test;
  reg [15:0] x, expected_out;
  wire [15:0] out;
  
  my_incrementer_16 a1(out, x);

  task assert_else_error;
    assert (out == expected_out) else $error("incrementer input was %b, out was %b but expected %b", x, out, expected_out);
  endtask

  initial begin
    x = 16'b0000000000000000; #1; expected_out = 16'b0000000000000001; #1; assert_else_error();
    x = 16'b0000000000000001; #1; expected_out = 16'b0000000000000010; #1; assert_else_error();
    x = 16'b0000000000000010; #1; expected_out = 16'b0000000000000011; #1; assert_else_error();
    x = 16'b0000000000000011; #1; expected_out = 16'b0000000000000100; #1; assert_else_error();
    x = 16'b0000111100001111; #1; expected_out = 16'b0000111100010000; #1; assert_else_error();
  end
endmodule