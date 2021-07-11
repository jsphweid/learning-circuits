`include "my_alu.sv"

module my_alu_test;
  reg [15:0] x, y;
  reg zx, nx, zy, ny, f, no;
  
  wire [15:0] out;
  wire zr, ng;
  reg [15:0] expected_out;
  reg expected_zr, expected_ng;

  my_alu a1(out, zr, ng, x, y, zx, nx, zy, ny, f, no);

  task assert_else_error;
    assert (out == expected_out && zr == expected_zr && ng == expected_ng) else $error("alu %b %b %b %b %b %b %b %b (%b %b) (%b %b) (%b %b)", x, y, zx, nx, zy, ny, f, no, out, expected_out, zr, expected_zr, ng, expected_ng);
  endtask

  initial begin
    // unconditional 0
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 0; zy = 1; ny = 0; f = 1; no = 0; #10; 
    expected_out = 16'b0000000000000000; expected_zr = 1; expected_ng = 0; assert_else_error();

    // unconditional 1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 1; ny = 1; f = 1; no = 1; #10; 
    expected_out = 16'b0000000000000001; expected_zr = 0; expected_ng = 0; assert_else_error();

    // unconditional -1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 1; ny = 0; f = 1; no = 0; #10; 
    expected_out = 16'b1111111111111111; expected_zr = 0; expected_ng = 1; assert_else_error();

    // x
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 1; ny = 1; f = 0; no = 0; #10; 
    expected_out = 16'b1010101010101010; expected_zr = 0; expected_ng = 1; assert_else_error();

    // y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 0; ny = 0; f = 0; no = 0; #10; 
    expected_out = 16'b1111000011110000; expected_zr = 0; expected_ng = 1; assert_else_error();

    // !x
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 1; ny = 1; f = 0; no = 1; #10; 
    expected_out = 16'b0101010101010101; expected_zr = 0; expected_ng = 0; assert_else_error();

    // !y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 0; ny = 0; f = 0; no = 1; #10; 
    expected_out = 16'b0000111100001111; expected_zr = 0; expected_ng = 0; assert_else_error();

    // -x
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 1; ny = 1; f = 1; no = 1; #10; 
    expected_out = 16'b0101010101010110; expected_zr = 0; expected_ng = 0; assert_else_error();

    // -y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 0; ny = 0; f = 1; no = 1; #10; 
    expected_out = 16'b0000111100010000; expected_zr = 0; expected_ng = 0; assert_else_error();

    // x + 1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 1; zy = 1; ny = 1; f = 1; no = 1; #10; 
    expected_out = 16'b1010101010101011; expected_zr = 0; expected_ng = 1; assert_else_error();

    // y + 1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 0; ny = 1; f = 1; no = 1; #10; 
    expected_out = 16'b1111000011110001; expected_zr = 0; expected_ng = 1; assert_else_error();

    // x - 1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 1; ny = 1; f = 1; no = 0; #10; 
    expected_out = 16'b1010101010101001; expected_zr = 0; expected_ng = 1; assert_else_error();

    // y - 1
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 1; nx = 1; zy = 0; ny = 0; f = 1; no = 0; #10; 
    expected_out = 16'b1111000011101111; expected_zr = 0; expected_ng = 1; assert_else_error();

    // x + y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 0; ny = 0; f = 1; no = 0; #10; 
    expected_out = 16'b1001101110011010; expected_zr = 0; expected_ng = 1; assert_else_error();

    // x - y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 1; zy = 0; ny = 0; f = 1; no = 1; #10; 
    expected_out = 16'b1011100110111010; expected_zr = 0; expected_ng = 1; assert_else_error();

    // y - x
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 0; ny = 1; f = 1; no = 1; #10; 
    expected_out = 16'b0100011001000110; expected_zr = 0; expected_ng = 0; assert_else_error();

    // x & y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 0; zy = 0; ny = 0; f = 0; no = 0; #10; 
    expected_out = 16'b1010000010100000; expected_zr = 0; expected_ng = 1; assert_else_error();

    // x | y
    x = 16'b1010101010101010; y = 16'b1111000011110000;
    zx = 0; nx = 1; zy = 0; ny = 1; f = 0; no = 1; #10; 
    expected_out = 16'b1111101011111010; expected_zr = 0; expected_ng = 1; assert_else_error();
  end

endmodule