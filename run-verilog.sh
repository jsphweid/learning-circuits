set -e

iverilog -o outs/nand.out verilog/nand.v
iverilog -o outs/nothing.out verilog/nothing.v
iverilog -o outs/relay.out verilog/relay.v
iverilog -o outs/relay_test.out verilog/relay.v verilog/relay_test.v
iverilog -o outs/two_relay_test.out verilog/relay.v verilog/two_relay_test.v
iverilog -o outs/relay_series_test.out verilog/relay.v verilog/relay_series_test.v
iverilog -o outs/relay_parallel_test.out verilog/relay.v verilog/relay_parallel_test.v
iverilog -o outs/latch_test.out verilog/latch.v verilog/latch_test.v
iverilog -o outs/nor_latch_test.out verilog/nor_latch.v verilog/nor_latch_test.v

vvp outs/nand.out
vvp outs/nothing.out
vvp outs/relay_test.out
vvp outs/two_relay_test.out
vvp outs/relay_series_test.out
vvp outs/relay_parallel_test.out
vvp outs/latch_test.out
vvp outs/nor_latch_test.out
