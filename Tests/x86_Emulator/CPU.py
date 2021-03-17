from VirtualRAM import Memory
from Instructions import *
import sys

class Flags:
    def __init__(self):
        self.Z = 0
        self.S = 0
        self.C = 0
        self.O = 0
        self.U = 0
        self.B = 0
        self.I = 0
        self.T = 0

    def PS(self):
        return self.Z << 7 + self.S << 6 + self.C << 5 + self.O << 4 + self.U << 3 + self.B << 2 + self.I >> 1 + self.T

class CPU:

    def __init__(self, memory: Memory, rVector=0x00008000):
        # Vectors
        self.Data = memory.Data
        self.Data[0x00000000] = (rVector & 0xFF000000) >> 24
        self.Data[0x00000001] = (rVector & 0xFF0000) >> 16
        self.Data[0x00000002] = (rVector & 0xFF00) >> 8
        self.Data[0x00000003] = rVector & 0xFF

        # Registers
        self.EAX = 0x00000000
        self.EDX = 0x00000000
        self.ECX = 0x00000000
        self.EBX = 0x00000000
        self.EBP = 0x00000000
        self.EDI = 0x00000000
        self.ESI = 0x00000000
        self.ESP = 0x00000000

        # Proccesor State
        self.PC = rVector
        self.SP = 0xFFFF
        self.PS = Flags()

        self.cycles = 0
        self.bitsize = 8

    def LoadProgram(self, prg) -> None:
        for i in range(len(prg)):
            if isinstance(prg[i], str):
                prg[i] = int(prg[i], 16)
            self.Data[i] = prg[i]
        self.PC = (prg[0] << 24) | (prg[1] << 16) | (prg[2] << 8) | prg[3]

    def __set_reg(self, code, value):
        '''Sets 32 bit register based on register code'''
        if code == 0:
            self.EAX = value
        elif code == 1:
            self.EBX = value
        elif code == 2:
            self.ECX = value
        elif code == 3:
            self.EDX = value
        elif code == 4:
            self.ESP = value
        elif code == 5:
            self.EBP = value
        elif code == 6:
            self.ESI = value
        elif code == 7:
            self.EDI = value

    def __get_reg(self, code):
        '''Gets 32 bit register based on register code'''
        registers = {
            0: self.EAX,
            1: self.EBX,
            2: self.ECX,
            3: self.EDX,
            4: self.ESP,
            5: self.EBP,
            6: self.ESI,
            7: self.EDI
        }
        return registers[code]

    def __ReadByte(self, address) -> int:
        '''Reads byte from memory, doesn't use cycles'''
        value = self.Data[address]
        return value

    def __FetchByte(self) -> int:
        '''Gets next byte in memory, and increments program counter'''
        value = self.Data[self.PC]
        self.PC += 1
        self.cycles -= 1
        return value

    def __FetchDWord(self) -> int:
        '''Gets the next 4 bytes as double word, and increments the program counter'''
        return self.FetchByte() << 24 | self.FetchByte() << 16 | self.FetchByte() << 8 | self.FetchByte()

    def __SysCall(self) -> None:
        '''Gets registers and performs syscall'''
        syscall = self.EAX
        if syscall == 0x1:
            output = self.EBX
            msg_point = self.ECX
            msg_len = self.EDX
            message = ''
            for i in range(msg_point, msg_point+msg_len):
                message += chr(self.Data[i])
            if output == 0x1:
                print(message)
        elif syscall == 0x0:
            ret = self.EBX
            if ret != 0x0:
                print("Exited with error: %s" % hex(ret))
            sys.exit()

    def Execute(self, cycles: int) -> int:
        '''Executes instructions limited on cycles. Cycles are consumed whenever the program couter is incremented. cycles == addresses'''
        self.cycles = cycles

        while self.cycles > 0:
            Ins = self.__FetchByte()
            Mod = self.__FetchByte()

            if Ins == INS_INT:
                if Mod == 0x1:
                    self.__SysCall()

            elif Ins == INS_MOV:
                reg1 = (Mod & 0b111000) >> 3
                if Mod & 0b11000000 == 0b10000000:
                    self.__set_reg(reg1, self.__FetchByte())
                elif Mod & 0b11000000 == 0b01000000:
                    self.__set_reg(reg1, self.__FetchByte())

        return cycles - self.cycles
