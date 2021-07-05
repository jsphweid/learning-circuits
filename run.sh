# cd n2t/verilog
rm -rf obj_dir
# ls -la
# verilator -Wall --cc my_computer.sv -I./ --exe ../../computer.cpp -LDFLAGS "-lmingw32 -lSDL2main -lSDL2"

# verilator -Wall --cc ./n2t/verilog/my_computer.sv -I./n2t/verilog --exe computer.cpp -LDFLAGS "-lmingw32 -lSDL2main -lSDL2"

# TODO: use `-Wall` instead of `-Wno-lint`
verilator -Wall --cc ./n2t/verilog/my_computer.sv -I./n2t/verilog --exe my_computer.cpp -LDFLAGS "-lmingw32 -lSDL2main -lSDL2"

# cd obj_dir
# make -f Vmy_computer.mk
# cd ..

# cd obj_dir
# make -f Vcomputer.mk
# cd ../
# ./05/obj_dir/Vcomputer.exe

