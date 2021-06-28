`ifndef my_mux
  `include "my_mux.sv"
`endif

module my_mux_16(out, a, b, sel);
  input [15:0] a, b;
  input sel;
  output [15:0] out;
  generate
    genvar i;
    for (i = 0; i <= 15; i++) begin
      my_mux m1(out[i], a[i], b[i], sel);
    end
  endgenerate
endmodule
