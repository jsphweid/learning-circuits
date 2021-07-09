`ifndef my_adder_16
  `include "my_adder_16.sv"
`endif
`ifndef my_mux_16
  `include "my_mux_16.sv"
`endif
`ifndef my_and_16
  `include "my_and_16.sv"
`endif
`ifndef my_or_8_way
  `include "my_or_8_way.sv"
`endif
`ifndef my_not_16
  `include "my_not_16.sv"
`endif
`define my_alu 1

module my_alu(out, zr, ng, x, y, zx, nx, zy, ny, f, no);
  input [15:0] x, y;
  input zx, nx, zy, ny, f, no;
  output [15:0] out;
  output zr, ng;

  // zx, zy
  wire zx_negated, zy_negated;
  wire [15:0] x_post_zx, y_post_zy;
  my_not n1(zx_negated, zx);
  my_not n2(zy_negated, zy);
  generate
    genvar i;
    for (i = 0; i <= 15; i++) begin
      my_and a1(x_post_zx[i], zx_negated, x[i]); // TODO: could we use my_and_16?
      my_and a2(y_post_zy[i], zy_negated, y[i]); // TODO: could we use my_and_16?
    end
  endgenerate

  // integer ff;
  // always @(*) begin
  //   ff = $fopen("output2.txt","a");
  //   $fwrite(ff,"alu: out %b, zr %b, ng %b, x %b, y %b, zx %b, nx %b, zy %b, ny %b, f %b, no %b\n", out, zr, ng, x, y, zx, nx, zy, ny, f, no);
  //   $fclose(ff);  
  // end

  // nx, ny
  wire [15:0] nx_out, ny_out, x_post_nx, x_post_ny;
  my_not_16 no01(nx_out, x_post_zx);
  my_not_16 no02(ny_out, y_post_zy);
  my_mux_16 m01(x_post_nx, x_post_zx, nx_out, nx);
  my_mux_16 m02(x_post_ny, y_post_zy, ny_out, ny);

  // f
  wire [15:0] sum_result, and_result, f_out;
  my_and_16 ba1(and_result, x_post_nx, x_post_ny);
  my_adder_16 badd1(sum_result, x_post_nx, x_post_ny);
  my_mux_16 m1(f_out, and_result, sum_result, f);
  
  // no
  wire [15:0] not_out;
  my_not_16 non1(not_out, f_out);
  my_mux_16 m2(out, f_out, not_out, no);

  // zr
  wire out_or_a_wire, out_or_b_wire, final_or_out;
  my_or_8_way o8w1(out_or_a_wire, out[7:0]);
  my_or_8_way o8w2(out_or_b_wire, out[15:8]);
  my_or oo1(final_or_out, out_or_a_wire, out_or_b_wire);
  my_not no1(zr, final_or_out);

  // ng
  assign ng = out[15]; // MSB indicates the sign...

endmodule