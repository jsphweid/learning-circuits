# learning circuits

This is just a repo that catalogs basic experiments in making simple emulated circuits in python and verilog. It is strictly educational for me and has little to no value outside of that.

This is also a repo where I put a lot of my creations from doing the nand2tetris (n2t) course.

# TODOs
- change title of repo to be more accurate

# n2t

Put projects/tools from n2t in a dir called `local/n2t` at the root of the directory so it looks like `local/n2t/projects/` and `local/n2t/tools` 

### Running python tests

```bash
pytest n2t/test_verilog.py
```


# Non-n2t stuff

### python

To run python tests, you need pytest installed in your environment then run:
```bash
PYTHONPATH=. pytest tests/
```