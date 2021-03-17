import cpu as CPU
import re

cpu = CPU.CPU()
with open('dist\\x86\\kernel.bin', 'rb') as f:
    contents = f.read()
    contents = re.findall("..", contents.hex())

cpu.LoadProgram(contents)
cpu.Execute()
