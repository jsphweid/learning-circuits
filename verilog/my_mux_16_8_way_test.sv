`include "my_mux_16_8_way.sv"

module my_mux_16_8_way_test;
  reg [15:0] a = 16'b1000000000000000, 
             b = 16'b0010000000000000, 
             c = 16'b0000100000000000, 
             d = 16'b0000001000000000,
             e = 16'b0000000010000000,
             f = 16'b0000000000100000,
             g = 16'b0000000000001000,
             h = 16'b0000000000000010,
             expected;
  reg [2:0] sel;
  wire [15:0] out;

  my_mux_16_8_way a1(out, a, b, c, d, e, f, g, h, sel);

  task assert_else_error;
    assert (expected == out) else $error("a was %b, b was %b, c was %b, d was %b... sel was %b, and out was %b but expected %b", a, b, c, d, sel, out, expected);
  endtask

  initial begin
    sel = 3'b000; #10; expected = 16'b1000000000000000; assert_else_error();
    sel = 3'b001; #10; expected = 16'b0010000000000000; assert_else_error();
    sel = 3'b010; #10; expected = 16'b0000100000000000; assert_else_error();
    sel = 3'b011; #10; expected = 16'b0000001000000000; assert_else_error();
    sel = 3'b100; #10; expected = 16'b0000000010000000; assert_else_error();
    sel = 3'b101; #10; expected = 16'b0000000000100000; assert_else_error();
    sel = 3'b110; #10; expected = 16'b0000000000001000; assert_else_error();
    sel = 3'b111; #10; expected = 16'b0000000000000010; assert_else_error();
  end

endmodule