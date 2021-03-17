from typing import Any

from InsCodes import *
from Memory import Memory


class Flags:
    def __init__(self):
        self.Z = 0 # Zero
        self.C = 0 # Carry
        self.O = 0 # Overflow
        self.S = 0 # Sign
        self.B = 0 # Busy
        self.T = 0 # Trap
        self.I = 0 # Interupt Disable
        self.E = 0 # Interupt

    def full(self):
        ps = self.Z << 7 | self.C << 6 | self.O << 5 | self.S << 4 | self.B << 3 | self.T << 2 | self.I << 1 | self.E
        return ps


class CPU:

    Syscall = 0x80
    COM0 = 0xF0001
    IntLoc = 0xF0000

    reserved      = 0x00
    InvalidOpcode = 0x06
    OutOfMemory   = 0x16

    def __init__(self):
        self.PC = 0x00000000 # Program Counter
        self.PS = Flags() # Processor Status

        self.Memory = Memory().Data
        self.Buffer = len(self.Memory) # 64 kb

        # 32-bit General
        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.EDI = 0
        self.ESI = 0
        self.ESP = 0 # Stack Pointer
        self.EBP = 0 # Base Pointer

        # 16-bit General
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0

        # 8-bit General
        self.BAX = 0
        self.BBX = 0
        self.BCX = 0
        self.BDX = 0

        self.Debug = False
        self.Cycles = 0
        self.InInterupt = False

    def LoadMemory(self, memory: Memory) -> None:
        self.Memory = memory.Data
        self.Buffer = len(self.Memory)

    def __FetchByte(self) -> int:
        byte = self.Memory[self.PC]
        self.PC += 1
        self.Cycles -= 1

        return byte

    def __FetchWord(self) -> int:
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __WriteReg(self, code: int, value: int) -> None:
        if code == Code_EAX:
            self.EAX = value

        elif code == Code_EBX:
            self.EBX = value

        elif code == Code_ECX:
            self.ECX = value

        elif code == Code_EDX:
            self.EDX = value

        self.Cycles -= 1

    def __HandleInterrupt(self) -> None:
        if self.Memory[self.IntLoc] == self.Syscall:
            self.__HandleSyscall()
        
        self.InInterupt = True
        self.PS.E = 0

    def Execute(self, cycles: int) -> Any:
        self.Cycles = cycles

        while (self.Cycles > 0):
            ins = self.__FetchByte()

            if ins == NOP:
                pass

            elif ins == MOV:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, value)

                elif mod == Addr_RegIm16:
                    reg = self.__FetchByte()
                    value = self.__FetchWord()
                    self.__WriteReg(reg, value)

            elif ins == INT:
                intCode = self.__FetchByte()
                self.Memory[self.IntLoc] = intCode
                self.__HandleInterrupt()

            elif ins == HLT:
                return

            else:
                print("InvalidOpcode: %s at address %s" % (hex(ins), hex(self.PC-1)))

        ret = None

        if self.Debug:
            ret = cycles - self.Cycles

        return ret
