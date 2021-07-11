`include "my_ram_512.sv"

module my_ram_512_test;
  reg [15:0] in;
  reg [8:0] addr;
  reg clk, load;
  wire [15:0] out;

  my_ram_512 r1(out, in, addr, clk, load);

  task assert_else_error(reg [15:0] exp);
    assert (out == exp) else $error("in: %d, addr: %b, clk: %b, load: %b, out: %d but expected %b", in, addr, clk, load, out, exp);
  endtask

  initial begin

    // reset
    clk = 0; load = 0; addr = 0; in = 0; #1;

    // write
    load = 1;
    in = 16'd2; addr = 9'b000000000; #1; clk = 1; #1; clk = 0;
    in = 16'd3; addr = 9'b000000001; #1; clk = 1; #1; clk = 0;
    in = 16'd4; addr = 9'b000000010; #1; clk = 1; #1; clk = 0;
    in = 16'd5; addr = 9'b000010011; #1; clk = 1; #1; clk = 0;
    in = 16'd6; addr = 9'b000001100; #1; clk = 1; #1; clk = 0;
    in = 16'd7; addr = 9'b001010101; #1; clk = 1; #1; clk = 0;
    in = 16'd8; addr = 9'b000000110; #1; clk = 1; #1; clk = 0;
    in = 16'd9; addr = 9'b110100111; #1; clk = 1; #1; clk = 0;
    in = 16'd1; addr = 9'b111111111; #1; clk = 1; #1; clk = 0;

    // read
    load = 0;
    #1; clk = 0; #1; addr = 9'b000000000; clk = 1; #1; assert_else_error(2);
    #1; clk = 0; #1; addr = 9'b000000001; clk = 1; #1; assert_else_error(3);
    #1; clk = 0; #1; addr = 9'b000000010; clk = 1; #1; assert_else_error(4);
    #1; clk = 0; #1; addr = 9'b000010011; clk = 1; #1; assert_else_error(5);
    #1; clk = 0; #1; addr = 9'b000001100; clk = 1; #1; assert_else_error(6);
    #1; clk = 0; #1; addr = 9'b001010101; clk = 1; #1; assert_else_error(7);
    #1; clk = 0; #1; addr = 9'b000000110; clk = 1; #1; assert_else_error(8);
    #1; clk = 0; #1; addr = 9'b110100111; clk = 1; #1; assert_else_error(9);
    #1; clk = 0; #1; addr = 9'b111111111; clk = 1; #1; assert_else_error(1);

  end
endmodule