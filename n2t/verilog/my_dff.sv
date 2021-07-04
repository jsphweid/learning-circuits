`define my_dff 1

module my_dff(out, in, clk);
  input in, clk;
  output reg out = 0;
  always @(posedge clk) begin
    out <= in;
  end
endmodule