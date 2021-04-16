import threading
import time

from CPU import *


def main():
    # Initilizing Memory and CPU
    cpu = CPU()
    # cpu.Debug = True
    mem = Memory(size=1048576)

    # Security so programs dont mess up ports
    mem.Data[0xFFFD] = JMPAHD
    mem.Data[0xFFFE] = Addr_Im8
    mem.Data[0xFFFF] = 11

    mem.Data[0x0000] = MOV
    mem.Data[0x0001] = Addr_RegIm8
    mem.Data[0x0002] = Code_EAX
    mem.Data[0x0003] = CPU.Sys_Time
    mem.Data[0x0004] = MOV
    mem.Data[0x0005] = Addr_RegIm8
    mem.Data[0x0006] = Code_EBX
    mem.Data[0x0007] = 0x0100 # oldtime
    mem.Data[0x0008] = INT
    mem.Data[0x0009] = 0x80
    mem.Data[0x000A] = INC
    mem.Data[0x000B] = Addr_Disp16
    mem.Data[0x000C] = 0x01 # oldtime
    mem.Data[0x000D] = 0x00

    # vars
    mem.Data[0x0100] = 0x00
    mem.Data[0x0101] = 0x00
    mem.Data[0x0102] = 0x00
    mem.Data[0x0103] = 0x00

    mem.Data[0x0104] = 0x00
    mem.Data[0x0105] = 0x00
    mem.Data[0x0106] = 0x00
    mem.Data[0x0107] = 0x00

    mem.Data[0x0108] = ord("D")
    mem.Data[0x0109] = ord("o")
    mem.Data[0x010A] = ord("n")
    mem.Data[0x010B] = ord("e")

    # loop
    mem.Data[0x000E] = MOV
    mem.Data[0x000F] = Addr_RegIm8
    mem.Data[0x0010] = Code_EAX
    mem.Data[0x0011] = CPU.Sys_Time
    mem.Data[0x0012] = MOV
    mem.Data[0x0013] = Addr_RegIm16
    mem.Data[0x0014] = Code_EBX
    mem.Data[0x0015] = 0x01
    mem.Data[0x0016] = 0x04
    mem.Data[0x0017] = INT
    mem.Data[0x0018] = 0x80

    mem.Data[0x0019] = CMP
    mem.Data[0x001A] = Addr_Disp16Disp16
    mem.Data[0x001B] = 0x01
    mem.Data[0x001C] = 0x00
    mem.Data[0x001D] = 0x01
    mem.Data[0x001E] = 0x04
    mem.Data[0x001F] = JNE
    mem.Data[0x0020] = Addr_Im8
    mem.Data[0x0021] = 0x0E # loop

    # Exit Protocal
    mem.Data[0x0022] = MOV
    mem.Data[0x0023] = Addr_RegIm8
    mem.Data[0x0024] = Code_EAX
    mem.Data[0x0025] = CPU.Sys_Write
    mem.Data[0x0026] = MOV
    mem.Data[0x0027] = Addr_RegIm8
    mem.Data[0x0028] = Code_EBX
    mem.Data[0x0029] = 0x01
    mem.Data[0x002A] = MOV
    mem.Data[0x002B] = Addr_RegIm16
    mem.Data[0x002C] = Code_ECX
    mem.Data[0x002D] = 0x01
    mem.Data[0x002E] = 0x08
    mem.Data[0x002F] = MOV
    mem.Data[0x0030] = Addr_RegIm8
    mem.Data[0x0031] = Code_EDX
    mem.Data[0x0032] = 0x04
    mem.Data[0x0033] = INT
    mem.Data[0x0034] = 0x80

    # Exit
    mem.Data[0x0035] = MOV
    mem.Data[0x0036] = Addr_RegIm8
    mem.Data[0x0037] = Code_EAX
    mem.Data[0x0038] = CPU.Sys_Exit
    mem.Data[0x0039] = MOV
    mem.Data[0x003A] = Addr_RegIm8
    mem.Data[0x003B] = Code_EBX
    mem.Data[0x003C] = 0x0
    mem.Data[0x003D] = INT
    mem.Data[0x003E] = 0x80

    # Start CPU
    cpu.LoadMemory(mem)
    cpu.Start()


if __name__ == "__main__":
    main()
