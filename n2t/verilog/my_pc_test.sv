`include "my_pc.sv"

module pc_tb();
  reg [15:0] in;
  reg load, inc, reset, clk;
  wire [15:0] out;

  my_pc pc1(out, in, load, inc, reset, clk);

  task assert_else_error(reg [15:0] exp_out);
      assert (out == exp_out) else begin
          $error("in %b load %b inc %b reset %b (out %b  exp_out %b)", in, load, inc, reset, out, exp_out);
      end
  endtask

  initial begin
    #1; clk = 0; 
    
    #1; in = 0; load = 0; inc = 0; reset = 0; #1; clk = 1; #1; assert_else_error(0);
    #1; in = 0; load = 0; inc = 0; reset = 0; #1; clk = 0; #1; assert_else_error(0);
    #1; in = 0; load = 0; inc = 1; reset = 0; #1; clk = 1; #1; assert_else_error(1);
    #1; in = 0; load = 0; inc = 1; reset = 0; #1; clk = 0; #1; assert_else_error(1);
    #1; in = -32123; load = 0; inc = 1; reset = 0; #1; clk = 1; #1; assert_else_error(2);
    #1; in = -32123; load = 0; inc = 1; reset = 0; #1; clk = 0; #1; assert_else_error(2);
    #1; in = -32123; load = 1; inc = 1; reset = 0; #1; clk = 1; #1; assert_else_error(-32123);
    #1; in = -32123; load = 1; inc = 1; reset = 0; #1; clk = 0; #1; assert_else_error(-32123);
    
    // experimental
    #1; in = -32123; load = 1; inc = 0; reset = 1; #1; clk = 1; #1; assert_else_error(0);
  end

endmodule
