`include "my_dmux_8_way.sv"

module my_dmux_8_way_test;
  reg in, a_expected, b_expected, c_expected, d_expected, e_expected, f_expected, g_expected, h_expected;
  reg [2:0] sel;
  wire a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out;

  my_dmux_8_way a1(a_out, b_out, c_out, d_out, e_out, f_out, g_out, h_out, in, sel);

  task assert_else_error;
    assert (a_expected == a_out && b_expected == b_out && c_expected == c_out && d_expected == d_out && 
            e_expected == e_out && f_expected == f_out && g_expected == g_out && h_expected == h_out) 
      else $error("in was %d, sel was %d, but output was not correct", in, sel);
  endtask

  initial begin
    in = 0; sel = 3'b000; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b000; #10; a_expected = 1; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b001; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b001; #10; a_expected = 0; b_expected = 1; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b010; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b010; #10; a_expected = 0; b_expected = 0; c_expected = 1; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b011; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b011; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 1; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b100; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b100; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 1; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b101; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b101; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 1; g_expected = 0; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b110; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b110; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 1; h_expected = 0; assert_else_error();
    in = 0; sel = 3'b111; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 0; assert_else_error();
    in = 1; sel = 3'b111; #10; a_expected = 0; b_expected = 0; c_expected = 0; d_expected = 0; 
                               e_expected = 0; f_expected = 0; g_expected = 0; h_expected = 1; assert_else_error();
  end
endmodule