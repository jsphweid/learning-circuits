`ifndef my_mux_16
  `include "my_mux_16.sv"
`endif

module my_mux_16_4_way(out, a, b, c, d, sel);
  input [15:0] a, b, c, d;
  input [1:0] sel;
  output [15:0] out;

  wire [15:0] w1, w2;
  my_mux_16 m1(w1, a, b, sel[0]);
  my_mux_16 m2(w2, c, d, sel[0]);
  my_mux_16 m3(out, w1, w2, sel[1]);

  // I think it's not too difficult to implement a better approach (as indicated in
  // most schematics for a 4-way multiplexer) but we need more generic components
  // like an `and` that combines n-signals all with different bus sizes
  // below is a start though...
  // wire most_not, least_not, a00, a01, a10, a11;
  // my_not n1(most_not, sel[1]); // msb
  // my_not n2(least_not, sel[0]); // lsb
  // my_and a1(a00, n1, n2);
  // my_and a2(a00, n1, sel[0]);
  // my_and a3(a00, n2, sel[1]);
  // my_and a4(a00, sel[0], sel[1]);

endmodule