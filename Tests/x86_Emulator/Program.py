from CPU import *
from VirtualRAM import Memory
import re

def main():
    mem = Memory()
    cpu = CPU(mem)
    prg = []

    with open("helloworld.o", "r") as f:
        contents = re.findall('........', f.read())

    for i in contents:
        prg.append(int(i, 2))

    cpu.LoadProgram(prg)
    cpu.Execute(80)

if __name__ == "__main__":
    main()
