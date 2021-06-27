set -e

iverilog -o build/nothing.out verilog/nothing.v
iverilog -o build/relay.out verilog/relay.v
iverilog -o build/relay_test.out verilog/relay.v verilog/relay_test.v
iverilog -o build/two_relay_test.out verilog/relay.v verilog/two_relay_test.v
iverilog -o build/relay_series_test.out verilog/relay.v verilog/relay_series_test.v
iverilog -o build/relay_parallel_test.out verilog/relay.v verilog/relay_parallel_test.v
iverilog -o build/latch_test.out verilog/latch.v verilog/latch_test.v
iverilog -o build/nor_latch_test.out verilog/nor_latch.v verilog/nor_latch_test.v
iverilog -o build/my_and_test.out verilog/my_and.sv verilog/my_and_test.v
iverilog -o build/my_or_test.out verilog/my_or.sv verilog/my_or_test.v

vvp build/nothing.out
vvp build/relay_test.out
vvp build/two_relay_test.out
vvp build/relay_series_test.out
vvp build/relay_parallel_test.out
vvp build/latch_test.out
vvp build/nor_latch_test.out
vvp build/my_and_test.out
vvp build/my_or_test.out
