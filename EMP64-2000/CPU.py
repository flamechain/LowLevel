import re

from Instructions import *
from Source import *


class CPUException(Exception):
    pass


class CPU:

    DivideError         = 0x0
    Debug               = 0x1
    Breakpoint          = 0x2
    Overflow            = 0x3
    InvalidOpcode       = 0x4
    DoubleFault         = 0x5
    SegmentNotPresent   = 0x6
    StackSegmentFault   = 0x7
    PageFault           = 0x8
    MathFault           = 0x9
    MachineCheck        = 0xA
    ProtectionException = 0xB
    SingleStepInterrupt = 0xC

    def __init__(self):
        self.RAX = 0x36d76289
        self.RBX = 0
        self.RCX = 0
        self.RDX = 0
        self.RDI = 0
        self.RSI = 0
        self.RBP = 0
        self.RSP = 0
        self.R8 = 0
        self.R9 = 0
        self.R10 = 0
        self.R11 = 0
        self.R12 = 0
        self.R13 = 0
        self.R14 = 0
        self.R15 = 0

        self.CS = 0
        self.DS = 0
        self.SS = 0

        self.OP = 0

        self.OUT = 0
        self.IN = 0

        self.EHR = 0b00001111

        self.RIP = 0
        self.FLAGS = FLAGS()
        self.FLAGS.IF = 1

        self.Buffer = 0
        self.Cycles = 0
        self.Memory = []

    def ForceExit(self):
        self.IN = 0xFF
        self.Memory[0] = SYSEXIT
        self.RIP = 0

    def LoadImage(self, filename: str):
        '''### Loads an iso image into RAM, from address 0

        ```
        cpu.LoadImage('kernel.iso')
        ```
        '''

        self.Memory = []

        with open(filename, 'rb') as f:
            contents = f.read().hex()
            contents = re.findall("..", contents)

        for i in contents:
            self.Memory.append(int(i, 16))

        self.Buffer = len(self.Memory)

    def LoadMemory(self, mem: Memory):
        '''### Loads a Memory() object into internal RAM

        ```
        from CPU import CPU
        from Source import Memory
        from Instruction import *

        cpu = CPU()
        mem = Memory()
        mem.Data[0] = HLT

        cpu.LoadMemory(mem)
        cpu.Start(0x0400)
        ```
        '''

        self.Memory = mem.Data
        self.Buffer = len(self.Memory)

    def Start(self, address: int):
        '''### Starts the execution of the CPU

        ```
        from CPU import CPU
        from Source import Memory
        from Instruction import *

        cpu = CPU()
        mem = Memory()
        mem.Data[0] = HLT

        cpu.LoadMemory(mem)
        cpu.Start(0x0400)
        ```
        '''

        self.RIP = address

        while True:
            self.__CheckForInterrupts()

            if self.FLAGS.TF:
                self.__JumpIDT(self.SingleStepInterrupt)

            prefix = 0
            self.OP = self.__FetchByte()

            if self.OP & 0b10000000:
                prefix = self.OP
                self.OP = self.__FetchByte()


            if self.OP == NOP:
                pass

            elif self.OP == UD:
                self.__JumpIDT(self.InvalidOpcode)

            elif self.OP == HLT:
                while True:
                    if self.__CheckForInterrupts():
                        break

            elif self.OP == SYSEXIT:
                return

            elif self.OP == Breakpoint:
                self.__JumpIDT(self.Breakpoint)

            elif self.OP == INT:
                self.__JumpIDT(self.__FetchByte())

            elif self.OP == MOV: # RegIm, RegReg, DispIm, DispReg
                if prefix & 0xF0 == Size8:
                    if prefix & 0xF == AddrRegIm:
                        reg = self.__FetchByte()
                        value = self.__FetchByte()
                        self.__SetReg(reg, value, size=8)

                    elif prefix & 0xF == AddrRegReg:
                        reg1 = self.__FetchByte()
                        reg2 = self.__FetchByte()
                        self.__SetReg(reg1, self.__GetReg(reg2, size=8), size=8)

                    elif prefix & 0xF == AddrDispIm:
                        address = self.__FetchQWord()
                        value = self.__FetchByte()
                        self.__WriteByte(address, value)

                    elif prefix & 0xF == AddrDispReg:
                        address = self.__FetchQWord()
                        reg = self.__GetReg(self.__FetchByte(), size=8)
                        self.__WriteByte(address, reg)

                elif prefix & 0xF0 == Size16:
                    if prefix & 0xF == AddrRegIm:
                        reg = self.__FetchByte()
                        value = self.__FetchWord()
                        self.__SetReg(reg, value, size=16)

                    elif prefix & 0xF == AddrRegReg:
                        reg1 = self.__FetchByte()
                        reg2 = self.__FetchByte()
                        self.__SetReg(reg1, self.__GetReg(reg2, size=16), size=16)

                    elif prefix & 0xF == AddrDispIm:
                        address = self.__FetchQWord()
                        value = self.__FetchWord()
                        self.__WriteWord(address, value)

                    elif prefix & 0xF == AddrDispReg:
                        address = self.__FetchQWord()
                        reg = self.__GetReg(self.__FetchByte(), size=16)
                        self.__WriteWord(address, reg)

                elif prefix & 0xF0 == Size32:
                    if prefix & 0xF == AddrRegIm:
                        reg = self.__FetchByte()
                        value = self.__FetchDWord()
                        self.__SetReg(reg, value, size=32)

                    elif prefix & 0xF == AddrRegReg:
                        reg1 = self.__FetchByte()
                        reg2 = self.__FetchByte()
                        self.__SetReg(reg1, self.__GetReg(reg2, size=32), size=32)

                    elif prefix & 0xF == AddrDispIm:
                        address = self.__FetchQWord()
                        value = self.__FetchDWord()
                        self.__WriteDWord(address, value)

                    elif prefix & 0xF == AddrDispReg:
                        address = self.__FetchQWord()
                        reg = self.__GetReg(self.__FetchByte(), size=32)
                        self.__WriteDWord(address, reg)

                elif prefix & 0xF0 == Size64:
                    if prefix & 0xF == AddrRegIm:
                        reg = self.__FetchByte()
                        value = self.__FetchQWord()
                        self.__SetReg(reg, value, size=64)

                    elif prefix & 0xF == AddrRegReg:
                        reg1 = self.__FetchByte()
                        reg2 = self.__FetchByte()
                        self.__SetReg(reg1, self.__GetReg(reg2, size=64), size=64)

                    elif prefix & 0xF == AddrDispIm:
                        address = self.__FetchQWord()
                        value = self.__FetchQWord()
                        self.__WriteQWord(address, value)

                    elif prefix & 0xF == AddrDispReg:
                        address = self.__FetchQWord()
                        reg = self.__GetReg(self.__FetchByte(), size=64)
                        self.__WriteQWord(address, reg)

            elif self.OP == CALL:
                self.__PushQWord(self.RIP)
                address = self.__FetchQWord()
                self.RIP = address

            elif self.OP == RET:
                self.RIP = self.__PopQWord()

            elif self.OP == CMP:
                

            else:
                self.__JumpIDT(self.InvalidOpcode)

    def __FetchByte(self) -> int:
        if self.RIP >= self.Buffer:
            self.RIP = 0

        value = self.Memory[self.RIP]
        self.Cycles += 1
        self.RIP += 1

        return value

    def __FetchWord(self) -> int:
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __FetchDWord(self) -> int:
        return self.__FetchWord() << 16 | self.__FetchWord()

    def __FetchQWord(self) -> int:
        return self.__FetchDWord() << 32 | self.__FetchDWord()

    def __CheckForInterrupts(self) -> bool:
        if self.IN:
            self.IN = 0
            return True

    def __JumpIDT(self, code: int):
        address = code * 4
        address = self.__ReadDWord(address)
        self.RIP = address

    def __ReadByte(self, addr: int) -> int:
        self.Cycles += 1
        return self.Memory[addr]

    def __ReadWord(self, addr: int) -> int:
        return self.__ReadByte(addr) << 8 | self.__ReadByte(addr+1)

    def __ReadDWord(self, addr: int) -> int:
        return self.__ReadWord(addr) << 16 | self.__ReadWord(addr+2)

    def __ReadQWord(self, addr: int) -> int:
        return self.__ReadDWord(addr) << 32 | self.__ReadDWord(addr+4)

    def __WriteByte(self, addr: int, value: int):
        self.Memory[addr] = value
        self.Cycles += 1

    def __WriteWord(self, addr: int, value: int):
        self.__WriteByte(addr, (value & 0xFF00) >> 8)
        self.__WriteByte(addr+1, value & 0xFF)

    def __WriteDWord(self, addr: int, value: int):
        self.__WriteWord(addr, (value & 0xFFFF0000) >> 16)
        self.__WriteWord(addr+2, value & 0xFFFF)

    def __WriteQWord(self, addr: int, value: int):
        self.__WriteDWord(addr, (value & 0xFFFFFFFF00000000) >> 32)
        self.__WriteDWord(addr+4, value & 0xFFFFFFFF)

    def __PushByte(self, value: int):
        self.Memory[self.RSP] = value
        self.RSP -= 1
        self.Cycles += 1

    def __PushWord(self, value: int):
        self.__PushByte((value & 0xFF00) >> 8)
        self.__PushByte(value & 0xFF)

    def __PushDWord(self, value: int):
        self.__PushWord((value & 0xFFFF0000) >> 16)
        self.__PushWord(value & 0xFFFF)

    def __PushQWord(self, value: int):
        self.__PushDWord((value & 0xFFFFFFFF00000000) >> 32)
        self.__PushDWord(value & 0xFFFFFFFF)

    def __PopByte(self) -> int:
        self.RSP += 1
        value = self.Memory[self.RSP]
        self.Cycles += 1

        return value

    def __PopWord(self) -> int:
        return self.__PopByte() << 8 | self.__PopByte()

    def __PopDWord(self) -> int:
        return self.__PopWord() << 16 | self.__PopWord()

    def __PopQWord(self) -> int:
        return self.__PopDWord() << 32 | self.__PopDWord()

    def __SetReg(self, code: int, value: int, size=64):
        if size == 8:
            segment = 0xFFFFFFFFFFFFFF00

        elif size == 16:
            segment = 0xFFFFFFFFFFFF0000

        elif size == 32:
            segment = 0xFFFFFFFF00000000

        elif size == 64:
            segment = 0

        if code == 0:
            self.RAX = (self.RAX & segment) | value

        if code == 1:
            self.RBX = (self.RBX & segment) | value

        if code == 2:
            self.RCX = (self.RCX & segment) | value

        if code == 3:
            self.RDX = (self.RDX & segment) | value

        if code == 4:
            self.RDI = (self.RDI & segment) | value

        if code == 5:
            self.RSI = (self.RSI & segment) | value

        if code == 6:
            self.RBP = (self.RBP & segment) | value

        if code == 7:
            self.RSP = (self.RSP & segment) | value

        if code == 8:
            self.R8 = (self.R8 & segment) | value

        if code == 9:
            self.R9 = (self.R9 & segment) | value

        if code == 10:
            self.R10 = (self.R10 & segment) | value

        if code == 11:
            self.R11 = (self.R11 & segment) | value

        if code == 12:
            self.R12 = (self.R12 & segment) | value

        if code == 13:
            self.R13 = (self.R13 & segment) | value

        if code == 14:
            self.R14 = (self.R14 & segment) | value

        if code == 15:
            self.R15 = (self.R15 & segment) | value

        self.Cycles += 1

    def __GetReg(self, code: int, size=64):
        if size == 8:
            segment = 0xFF

        elif size == 16:
            segment = 0xFFFF

        elif size == 32:
            segment = 0xFFFFFFFF

        elif size == 64:
            segment = 0xFFFFFFFFFFFFFFFF

        if code == 0:
            return self.RAX & segment

        if code == 1:
            return self.RBX & segment

        if code == 2:
            return self.RCX & segment

        if code == 3:
            return self.RDX & segment

        if code == 4:
            return self.RDI & segment

        if code == 5:
            return self.RSI & segment

        if code == 6:
            return self.RBP & segment

        if code == 7:
            return self.RSP & segment

        if code == 8:
            return self.R8 & segment

        if code == 9:
            return self.R9 & segment

        if code == 10:
            return self.R10 & segment

        if code == 11:
            return self.R11 & segment

        if code == 12:
            return self.R12 & segment

        if code == 13:
            return self.R13 & segment

        if code == 14:
            return self.R14 & segment

        if code == 15:
            return self.R15 & segment

        self.Cycles += 1
