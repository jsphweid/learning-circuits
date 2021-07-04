`include "my_ram_64.sv"

module my_ram_64_test;
  reg [15:0] in;
  reg [5:0] addr;
  reg clk, load;
  wire [15:0] out;

  my_ram_64 r1(out, in, addr, clk, load);

  task assert_else_error(reg [15:0] exp);
    assert (out == exp) else $error("in: %d, addr: %b, clk: %b, load: %b, out: %d but expected %b", in, addr, clk, load, out, exp);
  endtask

  initial begin

    // reset
    clk = 0; load = 0; addr = 0; in = 0; #1;

    // write
    load = 1;
    in = 16'd2; addr = 6'b000000; #1; clk = 1; #1; clk = 0;
    in = 16'd3; addr = 6'b000001; #1; clk = 1; #1; clk = 0;
    in = 16'd4; addr = 6'b000010; #1; clk = 1; #1; clk = 0;
    in = 16'd5; addr = 6'b010011; #1; clk = 1; #1; clk = 0;
    in = 16'd6; addr = 6'b001100; #1; clk = 1; #1; clk = 0;
    in = 16'd7; addr = 6'b010101; #1; clk = 1; #1; clk = 0;
    in = 16'd8; addr = 6'b000110; #1; clk = 1; #1; clk = 0;
    in = 16'd9; addr = 6'b100111; #1; clk = 1; #1; clk = 0;

    // read
    load = 0;
    #1; clk = 0; #1; addr = 6'b000000; clk = 1; #1; assert_else_error(2);
    #1; clk = 0; #1; addr = 6'b000001; clk = 1; #1; assert_else_error(3);
    #1; clk = 0; #1; addr = 6'b000010; clk = 1; #1; assert_else_error(4);
    #1; clk = 0; #1; addr = 6'b010011; clk = 1; #1; assert_else_error(5);
    #1; clk = 0; #1; addr = 6'b001100; clk = 1; #1; assert_else_error(6);
    #1; clk = 0; #1; addr = 6'b010101; clk = 1; #1; assert_else_error(7);
    #1; clk = 0; #1; addr = 6'b000110; clk = 1; #1; assert_else_error(8);
    #1; clk = 0; #1; addr = 6'b100111; clk = 1; #1; assert_else_error(9);

  end
endmodule