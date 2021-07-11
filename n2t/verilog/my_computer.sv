`ifndef my_cpu
  `include "my_cpu.sv"
`endif
`ifndef my_rom_32k
  `include "my_rom_32k.sv"
`endif
`ifndef my_memory
  `include "my_memory.sv"
`endif
`define my_computer 1

module my_computer(reset, clk);
  input reset, clk;

  wire [15:0] rom_out_instruction, cpu_out_m, memory_out;
  wire [14:0] cpu_out_pc, cpu_out_address_m;
  wire cpu_out_write_m;

  // outM, writeM, addressM, pc, inM, instruction, clk, reset
  my_cpu cpu(cpu_out_m, cpu_out_write_m, cpu_out_address_m, cpu_out_pc, memory_out, rom_out_instruction, clk, reset);

  // out, addr
  my_rom_32k rom(rom_out_instruction, cpu_out_pc);

  // out, in, addr, clk, load
  my_memory ram(memory_out, cpu_out_m, cpu_out_address_m, !clk, cpu_out_write_m);
endmodule