`ifndef my_dff
  `include "my_dff.sv"
`endif
`ifndef my_mux
  `include "my_mux.sv"
`endif

`define my_1_bit_register

module my_1_bit_register(out, in, clk, load);
  input in, clk, load;
  output out;
  wire mux_output;
  my_mux mux1(mux_output, out, in, load);
  my_dff dff1(out, mux_output, clk);
endmodule
