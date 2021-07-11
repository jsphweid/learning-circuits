# nand2tetris

My friend Brian suggested this course as a way to learn a computer really really works. I bought the ebook and started running through it and basically got really into it. I created this repo to house all the things I built along the course.

# Setup and run

### tests

Prep:
1. put projects/tools from n2t in a dir called `local/n2t` at the root of the directory so it looks like `local/n2t/projects/` and `local/n2t/tools`
2. make the bash tools executable with `chmod +x local/n2t/tools/CPUEmulator.sh` for example

Then run:
- `pip install -r requirements.txt`
- `PYTHONPATH=. pytest tests`

NOTE: make sure you run it from the root directory (working directory is the root folder)
