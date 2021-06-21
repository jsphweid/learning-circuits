set -e

iverilog -o outs/nand.out verilog/nand.v
iverilog -o outs/nothing.out verilog/nothing.v
# iverilog -o outs/relay_out.out verilog/relay.v

vvp outs/nand.out
vvp outs/nothing.out
# vvp outs/relay_out.out
