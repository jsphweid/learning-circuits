# learning circuits

This is just a repo that catalogs basic experiments in making simple emulated circuits in python and verilog. It is strictly educational for me and has little to no value outside of that.

# running

### verilog

To compile verilog modules and tests, just run:
```bash
run-verilog.sh
```

### python

To run python tests, you need pytest installed in your environment then run:
```bash
PYTHONPATH=. pytest tests/
```