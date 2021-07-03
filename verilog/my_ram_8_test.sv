`include "my_ram_8.sv"

module my_ram_8_test;
  reg [15:0] in;
  reg [2:0] addr;
  reg clk, load;
  wire [15:0] out;

  my_ram_8 r1(out, in, addr, clk, load);

  task assert_else_error(exp);
    assert (out == exp) else $error("in: %d, addr: %b, clk: %b, load: %b, out: %d but expected %b", in, addr, clk, load, out, exp);
  endtask

  initial begin
    // reset
    clk = 0; load = 0; addr = 0; in = 0; #1;

    // write
    load = 1;
    in = 2; addr = 3'b000; #1; clk = 1; #1;
    in = 3; addr = 3'b001; #1; clk = 1; #1;
    in = 4; addr = 3'b010; #1; clk = 1; #1;
    in = 5; addr = 3'b011; #1; clk = 1; #1;
    in = 6; addr = 3'b100; #1; clk = 1; #1;
    in = 7; addr = 3'b101; #1; clk = 1; #1;
    in = 8; addr = 3'b110; #1; clk = 1; #1;
    in = 9; addr = 3'b111; #1; clk = 1; #1;

    // read
    load = 0;
    #1; clk = 0; #1; addr = 3'b000; clk = 1; #1; assert_else_error(2);
    #1; clk = 0; #1; addr = 3'b001; clk = 1; #1; assert_else_error(3);
    #1; clk = 0; #1; addr = 3'b010; clk = 1; #1; assert_else_error(4);
    #1; clk = 0; #1; addr = 3'b011; clk = 1; #1; assert_else_error(5);
    #1; clk = 0; #1; addr = 3'b100; clk = 1; #1; assert_else_error(6);
    #1; clk = 0; #1; addr = 3'b101; clk = 1; #1; assert_else_error(7);
    #1; clk = 0; #1; addr = 3'b110; clk = 1; #1; assert_else_error(8);
    #1; clk = 0; #1; addr = 3'b111; clk = 1; #1; assert_else_error(9);
  end

endmodule