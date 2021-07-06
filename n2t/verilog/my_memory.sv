`ifndef my_ram_16k
  `include "my_ram_16k.sv"
`endif
`ifndef my_mux_16
  `include "my_mux_16.sv"
`endif
`include "my_screen.sv"
`define my_memory 1

module my_memory(out, in, addr, clk, load);
  input [15:0] in;
  input [14:0] addr;
  input clk, load;
  output [15:0] out;

  wire [15:0] ram_out, screen_out;
  wire address_is_keyboard_or_screen = addr[14];
  wire address_is_screen = address_is_keyboard_or_screen && !addr[13];
  wire address_is_main_ram = !address_is_screen;
  wire address_is_keyboard = addr == 15'b110000000000000;
  wire load_screen = address_is_screen && load;
  wire load_main_ram = address_is_main_ram && load;
  my_ram_16k ram1(ram_out, in, addr[13:0], clk, load_main_ram);
  my_screen screen(screen_out, in, addr[12:0], clk, load_screen);
  reg [15:0] scancode /*verilator public*/;

  wire [15:0] keyboard_screen_out;
  my_mux_16 o1(keyboard_screen_out, screen_out, scancode, address_is_keyboard);
  my_mux_16 o2(out, ram_out, keyboard_screen_out, address_is_keyboard_or_screen);

endmodule