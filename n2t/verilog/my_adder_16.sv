`ifndef my_full_adder
  `include "my_full_adder.sv"
`endif
`ifndef my_half_adder
  `include "my_half_adder.sv"
`endif
`define my_adder_16 1

module my_adder_16(out, a, b);
  input [15:0] a, b;
  output [15:0] out;
  
    wire carry_0;
    wire carry_1;
    wire carry_2;
    wire carry_3;
    wire carry_4;
    wire carry_5;
    wire carry_6;
    wire carry_7;
    wire carry_8;
    wire carry_9;
    wire carry_10;
    wire carry_11;
    wire carry_12;
    wire carry_13;
    wire carry_14;
    /* verilator lint_off UNUSED */
    wire carry_15;

    my_half_adder half_add(out[0], carry_0, a[0], b[0]);
    my_full_adder _1_full_add(out[1], carry_1, a[1], b[1], carry_0);    
    my_full_adder _2_full_add(out[2], carry_2, a[2], b[2], carry_1);    
    my_full_adder _3_full_add(out[3], carry_3, a[3], b[3], carry_2);    
    my_full_adder _4_full_add(out[4], carry_4, a[4], b[4], carry_3);    
    my_full_adder _5_full_add(out[5], carry_5, a[5], b[5], carry_4);    
    my_full_adder _6_full_add(out[6], carry_6, a[6], b[6], carry_5);    
    my_full_adder _7_full_add(out[7], carry_7, a[7], b[7], carry_6);    
    my_full_adder _8_full_add(out[8], carry_8, a[8], b[8], carry_7);    
    my_full_adder _9_full_add(out[9], carry_9, a[9], b[9], carry_8);    
    my_full_adder _10_full_add(out[10], carry_10, a[10], b[10], carry_9);    
    my_full_adder _11_full_add(out[11], carry_11, a[11], b[11], carry_10);    
    my_full_adder _12_full_add(out[12], carry_12, a[12], b[12], carry_11);    
    my_full_adder _13_full_add(out[13], carry_13, a[13], b[13], carry_12);    
    my_full_adder _14_full_add(out[14], carry_14, a[14], b[14], carry_13);    
    my_full_adder _15_full_add(out[15], carry_15, a[15], b[15], carry_14);    
    
endmodule