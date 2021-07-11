`include "my_mux_16.sv"

module my_mux_16_test();
  reg [15:0] a, b;
  reg sel;
  reg [15:0] expected;
  wire [15:0] out;

  my_mux_16 a1(out, a, b, sel);

  task assert_else_error;
    assert (expected == out) else $error("a was %b, b was %b, sel was %b, out was %b but expected %b\n", a, b, sel, out, expected);
  endtask

  initial begin
    a = 16'b0000001010110010; b = 16'b1100110011001100; sel = 0; #10; 
      expected = 16'b0000001010110010; assert_else_error();
    a = 16'b0000001010110010; b = 16'b1100110011001100; sel = 1; #10; 
      expected = 16'b1100110011001100; assert_else_error();
  end
endmodule
