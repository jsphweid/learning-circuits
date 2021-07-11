`include "my_ram_4k.sv"

module my_ram_4k_test;
  reg [15:0] in;
  reg [11:0] addr;
  reg clk, load;
  wire [15:0] out;

  my_ram_4k r1(out, in, addr, clk, load);

  task assert_else_error(reg [15:0] exp);
    assert (out == exp) else $error("in: %d, addr: %b, clk: %b, load: %b, out: %d but expected %b", in, addr, clk, load, out, exp);
  endtask

  initial begin

    // reset
    clk = 0; load = 0; addr = 0; in = 0; #1;

    // write
    load = 1;
    in = 16'd2; addr = 12'b000000000000; #1; clk = 1; #1; clk = 0;
    in = 16'd9; addr = 12'b000110100111; #1; clk = 1; #1; clk = 0;
    in = 16'd1; addr = 12'b111111111111; #1; clk = 1; #1; clk = 0;

    // read
    load = 0;
    #1; clk = 0; #1; addr = 12'b000000000000; clk = 1; #1; assert_else_error(2);
    #1; clk = 0; #1; addr = 12'b000110100111; clk = 1; #1; assert_else_error(9);
    #1; clk = 0; #1; addr = 12'b111111111111; clk = 1; #1; assert_else_error(1);

  end
endmodule