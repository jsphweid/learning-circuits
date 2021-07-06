set -e

rm -rf obj_dir

verilator -Wall --cc ./n2t/verilog/my_computer.sv -I./n2t/verilog --exe my_computer.cpp -LDFLAGS "-lSDL2main -lSDL2"
cd obj_dir
make -f Vmy_computer.mk

cd ..
./obj_dir/Vmy_computer
