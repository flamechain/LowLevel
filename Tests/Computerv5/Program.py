from CPU import *
from VirtualRAM import Memory

def main():
    mem = Memory()
    cpu = CPU(mem)
    cpu.ECX = 1
    cpu.EBX = 1
    cpu.EDI = 1
    cpu.Data[0x8000] = INS_ADD | 0b11
    cpu.Data[0x8001] = 0b00_001_100
    cpu.Data[0x8002] = 0b10_111_011
    cpu.Execute(3)
    print(cpu.ECX)

main()

mem = Memory()
cpu = CPU(mem)
