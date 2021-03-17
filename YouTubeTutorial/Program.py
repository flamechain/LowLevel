from Memory import Memory
from CPU import CPU
from InsCodes import *


def main():
    memory = Memory(size=0xF000F)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x00] = INT
    memory.Data[0x01] = 0x1

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(2)
    print(cycles)


if __name__ == "__main__":
    main()
