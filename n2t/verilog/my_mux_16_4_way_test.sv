`include "my_mux_16_4_way.sv"

module my_mux_16_4_way_test;
  reg [15:0] a = 16'b1000000000000000, 
             b = 16'b0000100000000000, 
             c = 16'b0000000010000000, 
             d = 16'b0000000000001000,
             expected;
  reg [1:0] sel;
  wire [15:0] out;

  my_mux_16_4_way a1(out, a, b, c, d, sel);

  task assert_else_error;
    assert (expected == out) else $error("a was %b, b was %b, c was %b, d was %b... sel was %b, and out was %b but expected %b", a, b, c, d, sel, out, expected);
  endtask

  initial begin
    sel = 2'b00; #10; expected = 16'b1000000000000000; assert_else_error();
    sel = 2'b01; #10; expected = 16'b0000100000000000; assert_else_error();
    sel = 2'b10; #10; expected = 16'b0000000010000000; assert_else_error();
    sel = 2'b11; #10; expected = 16'b0000000000001000; assert_else_error();
  end

endmodule
