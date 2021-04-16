from CPU import CPU
from Codes import *
from Source import Memory
import sys

def writefile(filename='main'):
    binary = bytearray()
    mem = Memory(0x2B)

    # Program Here
    mem.Data[0x0] = Pre_8 | Addr_RegIm
    mem.Data[0x1] = MOV
    mem.Data[0x2] = Reg_RAX
    mem.Data[0x3] = CPU.Sys_Read
    mem.Data[0x4] = Pre_8 | Addr_RegIm
    mem.Data[0x5] = MOV
    mem.Data[0x6] = Reg_RDI
    mem.Data[0x7] = 1
    mem.Data[0x8] = Pre_8 | Addr_RegIm
    mem.Data[0x9] = MOV
    mem.Data[0xA] = Reg_RSI
    mem.Data[0xB] = 0xFF
    mem.Data[0xC] = Pre_8 | Addr_RegIm
    mem.Data[0xD] = MOV
    mem.Data[0xE] = Reg_RDX
    mem.Data[0xF] = 14
    mem.Data[0x10] = SYSCALL
    mem.Data[0x11] = Pre_8 | Addr_RegIm
    mem.Data[0x12] = MOV
    mem.Data[0x13] = Reg_RAX
    mem.Data[0x14] = CPU.Sys_Write
    mem.Data[0x15] = Pre_8 | Addr_RegIm
    mem.Data[0x16] = MOV
    mem.Data[0x17] = Reg_RDI
    mem.Data[0x18] = 1
    mem.Data[0x19] = Pre_8 | Addr_RegIm
    mem.Data[0x1A] = MOV
    mem.Data[0x1B] = Reg_RSI
    mem.Data[0x1C] = 0xFF
    mem.Data[0x1D] = Pre_8 | Addr_RegIm
    mem.Data[0x1E] = MOV
    mem.Data[0x1F] = Reg_RDX
    mem.Data[0x20] = 14
    mem.Data[0x21] = SYSCALL
    mem.Data[0x22] = Pre_8 | Addr_RegIm
    mem.Data[0x23] = MOV
    mem.Data[0x24] = Reg_RAX
    mem.Data[0x25] = CPU.Sys_Exit
    mem.Data[0x26] = Pre_8 | Addr_RegIm
    mem.Data[0x27] = MOV
    mem.Data[0x28] = Reg_RDI
    mem.Data[0x29] = 0
    mem.Data[0x2A] = SYSCALL
    # End Program

    for i in mem.Data:
        binary.extend(bytes([i]))

    with open(filename + '.bin', 'wb') as f:
        f.write(binary)

def main():
    mem = Memory(0x10000)
    cpu = CPU()

    cpu.LoadMemory(mem)
    cpu.LoadProgram('helloworld', 0x0)
    cpu.Start()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mem = Memory(0x10000)
        cpu = CPU()
        cpu.LoadMemory(mem)
        cpu.LoadProgram(sys.argv[1], 0x0)
        cpu.Start()

    else:
        main()
