import re

from Encodings import *

class Flags:
    def __init__(self):
        self.CF = 0
        self.ZF = 0
        self.OF = 0
        self.SF = 0
        self.TF = 0
        self.IF = 0
        self.IO = 0
        self.PL = 0

    def full(self) -> int:
        return self.CF << 7 | self.ZF << 6 | self.OF << 5 | self.SF << 4 | self.TF << 3 | self.IF << 2 | self.IO << 1 | self.PL

    def set(self, value: int):
        self.CF = value & 0x10000000 >> 7
        self.ZF = value & 0x1000000 >> 6
        self.OF = value & 0x100000 >> 5
        self.SF = value & 0x10000 >> 4
        self.TF = value & 0x1000 >> 3
        self.IF = value & 0x100 >> 2
        self.IO = value & 0x10 >> 1
        self.PL = value & 0x1

class CPUInterrupt(Exception):
    pass

class CPU:

    UnknownException        = 0x0
    SingleStepInterrupt     = 0x1
    Breakpoint              = 0x2
    DivideByZeroError       = 0x3
    Debug                   = 0x4
    NonMaskableInterrupt    = 0x5
    StackOverflow           = 0x6
    StackUnderflow          = 0x7
    InvalidOpcode           = 0x8
    DoubleFault             = 0x9
    PageFault               = 0xA
    FloatingPointException  = 0xB
    MachineCheck            = 0xC
    TripleFault             = 0xD

    def __init__(self):
        self.Memory = []
        self.__exit = False

        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.EDI = 0
        self.ESI = 0
        self.EBP = 0xb0000
        self.ESP = 0xb0000

        self.EIP = 2
        self.FLAGS = Flags()
        self.IO = 0

    def Boot(self, filename: str):
        with open(filename, 'rb') as f:
            contents = f.read().hex()
            contents = re.findall("..", contents)

        for i in contents:
            self.Memory.append(int(i, 16))

        while True:
            try:
                self.__Execute()

            except CPUInterrupt as e:
                if int(str(e)) == 0:
                    return

                print(e, self.EAX)
                self.EIP = self.__ReadDWord(512 + int(str(e))*4)

    def RaiseInterrupt(self, code: int, **kwargs):
        if 'opcode' in kwargs:
            self.EAX = kwargs['opcode']

        raise CPUInterrupt(code)

    def Shutdown(self):
        self.__exit = True

    def __Execute(self):
        while True:
            if self.__exit:
                raise CPUInterrupt(0)

            if self.FLAGS.TF:
                self.RaiseInterrupt(self.SingleStepInterrupt)

            ins = self.__FetchByte()

            if ins == 0xCC:
                self.RaiseInterrupt(self.Breakpoint)

            elif ins == JMP:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModIm:
                    if (mod & 0b1100) >> 2 == Size32:
                        self.EIP = self.__FetchDWord()

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.EIP = self.__FetchWord()

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.EIP = self.__FetchByte()

            elif ins == CALL:
                mod = self.__FetchByte()
                oldEIP = self.EIP

                if (mod & 0xF0) >> 4 == ModIm:
                    if (mod & 0b1100) >> 2 == Size32:
                        self.EIP = self.__FetchDWord()
                        oldEIP += 4

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.EIP = self.__FetchWord()
                        oldEIP += 2

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.EIP = self.__FetchByte()
                        oldEIP += 1

                self.__PushDWord(oldEIP)

            elif ins == RET:
                self.EIP = self.__PopDWord()

            elif ins == PUSH:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModReg:
                    reg = self.__FetchByte()
                    value = self.__ReadReg(reg)

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__PushDWord(value)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__PushWord(value & 0xFFFF)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__PushByte(value & 0xFF)

                elif (mod & 0xF0) >> 4 == ModIm:
                    if (mod & 0b1100) >> 2 == Size32:
                        value = self.__FetchDWord()
                        self.__PushDWord(value)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value = self.__FetchWord()
                        self.__PushWord(value)

                    elif (mod & 0b1100) >> 2 == Size8:
                        value = self.__FetchByte()
                        self.__PushByte(value)

            elif ins == POP:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModReg:
                    reg = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg, self.__PopDWord(), 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg, self.__PopWord(), 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg, self.__PopByte(), 8)

            elif ins == ADD:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegReg:
                    reg1 = self.__FetchByte()
                    reg2 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__ReadReg(reg2)

                    elif mod & 0b11 == Size16:
                        value2 = self.__ReadReg(reg2) & 0xFFFF

                    elif mod & 0b11 == Size8:
                        value2 = self.__ReadReg(reg2) & 0xFF

                    value = value1 + value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg1, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg1, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg1, value, 8)

            elif ins == MUL:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegReg:
                    reg1 = self.__FetchByte()
                    reg2 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__ReadReg(reg1)

                    elif mod & 0b11 == Size16:
                        value2 = self.__ReadReg(reg1) & 0xFFFF

                    elif mod & 0b11 == Size8:
                        value2 = self.__ReadReg(reg1) & 0xFF

                    value = value1 * value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg1, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg1, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg1, value, 8)

                elif (mod & 0xF0) >> 4 == ModRegIm:
                    reg = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__FetchDWord()

                    elif mod & 0b11 == Size16:
                        value2 = self.__FetchWord()

                    elif mod & 0b11 == Size8:
                        value2 = self.__FetchByte()

                    value = value1 * value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg, value, 8)

            elif ins == OR:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegIm:
                    reg1 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__FetchDWord()

                    elif mod & 0b11 == Size16:
                        value2 = self.__FetchWord()

                    elif mod & 0b11 == Size8:
                        value2 = self.__FetchByte()

                    value = value1 | value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg1, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg1, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg1, value, 8)

            elif ins == XOR:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegReg:
                    reg1 = self.__FetchByte()
                    reg2 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__ReadReg(reg1)

                    elif mod & 0b11 == Size16:
                        value2 = self.__ReadReg(reg1) & 0xFFFF

                    elif mod & 0b11 == Size8:
                        value2 = self.__ReadReg(reg1) & 0xFF

                    value = value1 ^ value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg1, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg1, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg1, value, 8)

            elif ins == INC:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModReg:
                    reg = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value = self.__ReadReg(reg)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value = self.__ReadReg(reg) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value = self.__ReadReg(reg) & 0xFF

                    value += 1

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg, value, 8)

            elif ins == SHUTDWN:
                self.__exit = True

            elif ins == SAL:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegIm:
                    reg1 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__FetchDWord()

                    elif mod & 0b11 == Size16:
                        value2 = self.__FetchWord()

                    elif mod & 0b11 == Size8:
                        value2 = self.__FetchByte()

                    value = value1 << value2

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg1, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg1, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg1, value, 8)

            elif ins == CMP:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegIm:
                    reg1 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        value1 = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        value1 = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        value1 = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value2 = self.__FetchDWord()

                    elif mod & 0b11 == Size16:
                        value2 = self.__FetchWord()

                    elif mod & 0b11 == Size8:
                        value2 = self.__FetchByte()

                    value = value1 - value2

                    if value == 0:
                        self.FLAGS.ZF = 1

                    elif value < 0:
                        self.FLAGS.SF = 1

            elif ins == JE:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModIm:
                    if (mod & 0b1100) >> 2 == Size32:
                        addr = self.__FetchDWord()

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr = self.__FetchWord()

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr = self.__FetchByte()

                if self.FLAGS.ZF == 1:
                    self.EIP = addr

            elif ins == MOV:
                mod = self.__FetchByte()

                if (mod & 0xF0) >> 4 == ModRegIm:
                    reg = self.__FetchByte()

                    if mod & 0b11 == Size32:
                        value = self.__FetchDWord()

                    elif mod & 0b11 == Size16:
                        value = self.__FetchWord()

                    elif mod & 0b11 == Size8:
                        value = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        self.__WriteReg(reg, value, 32)

                    elif (mod & 0b1100) >> 2 == Size16:
                        self.__WriteReg(reg, value, 16)

                    elif (mod & 0b1100) >> 2 == Size8:
                        self.__WriteReg(reg, value, 8)

                elif (mod & 0xF0) >> 4 == ModDispReg:
                    if (mod & 0b1100) >> 2 == Size32:
                        addr = self.__FetchDWord()

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr = self.__FetchWord()

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr = self.__FetchByte()

                    reg = self.__FetchByte()

                    if mod & 0b11 == Size32:
                        value = self.__ReadReg(reg)
                        self.__WriteDWord(addr, value)

                    elif mod & 0b11 == Size16:
                        value = self.__ReadReg(reg) & 0xFFFF
                        self.__WriteWord(addr, value)

                    elif mod & 0b11 == Size8:
                        value = self.__ReadReg(reg) & 0xFF
                        self.__WriteByte(addr, value)                    

                elif (mod & 0xF0) >> 4 == ModDispIm:
                    if (mod & 0b1100) >> 2 == Size32:
                        addr = self.__FetchDWord()

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr = self.__FetchWord()

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr = self.__FetchByte()

                    if mod & 0b11 == Size32:
                        value = self.__FetchDWord()
                        self.__WriteDWord(addr, value)

                    elif mod & 0b11 == Size16:
                        value = self.__FetchWord()
                        self.__WriteWord(addr, value)

                    elif mod & 0b11 == Size8:
                        value = self.__FetchByte()
                        self.__WriteByte(addr, value)

                elif (mod & 0xF0) >> 4 == ModDispDisp:
                    if (mod & 0b1100) >> 2 == Size32:
                        addr1 = self.__FetchDWord()

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr1 = self.__FetchWord()

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr1 = self.__FetchByte()

                    if mod & 0b11 == Size32:
                        addr2 = self.__FetchDWord()
                        value = self.__ReadByte(addr2)
                        self.__WriteByte(addr1, value)

                    elif mod & 0b11 == Size16:
                        addr2 = self.__FetchWord()
                        value = self.__ReadByte(addr2)
                        self.__WriteByte(addr1, value)

                    elif mod & 0b11 == Size8:
                        addr2 = self.__FetchByte()
                        value = self.__ReadByte(addr2)
                        self.__WriteByte(addr1, value)

                elif (mod & 0xF0) >> 4 == ModRegdispReg:
                    reg1 = self.__FetchByte()
                    reg2 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        addr = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        value = self.__ReadReg(reg2)
                        self.__WriteDWord(addr, value)

                    elif mod & 0b11 == Size16:
                        value = self.__ReadReg(reg2) & 0xFFFF
                        self.__WriteWord(addr, value)

                    elif mod & 0b11 == Size8:
                        value = self.__ReadReg(reg2) & 0xFF
                        self.__WriteByte(addr, value)

                elif (mod & 0xF0) >> 4 == ModRegdispRegdisp:
                    reg1 = self.__FetchByte()
                    reg2 = self.__FetchByte()

                    if (mod & 0b1100) >> 2 == Size32:
                        addr = self.__ReadReg(reg1)

                    elif (mod & 0b1100) >> 2 == Size16:
                        addr = self.__ReadReg(reg1) & 0xFFFF

                    elif (mod & 0b1100) >> 2 == Size8:
                        addr = self.__ReadReg(reg1) & 0xFF

                    if mod & 0b11 == Size32:
                        addr = self.__ReadReg(reg2)
                        value = self.__ReadByte(addr)
                        self.__WriteByte(addr, value)

                    elif mod & 0b11 == Size16:
                        addr = self.__ReadReg(reg2) & 0xFFFF
                        value = self.__ReadByte(addr)
                        self.__WriteByte(addr, value)

                    elif mod & 0b11 == Size8:
                        addr = self.__ReadReg(reg2) & 0xFF
                        value = self.__ReadByte(addr)
                        self.__WriteByte(addr, value)

            else:
                self.RaiseInterrupt(self.InvalidOpcode, opcode=ins)

    def __FetchByte(self) -> int:
        value = self.Memory[self.EIP]
        self.EIP += 1

        if self.EIP >= len(self.Memory):
            self.EIP = 0

        return value

    def __FetchWord(self) -> int:
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __FetchDWord(self) -> int:
        return self.__FetchWord() << 16 | self.__FetchWord()

    def __PushByte(self, value: int):
        self.Memory[self.ESP] = value & 0xFF
        self.ESP += 1

        if self.ESP > (self.EBP + 4096):
            self.RaiseInterrupt(self.StackOverflow)

    def __PushWord(self, value: int):
        self.__PushByte((value & 0xFF00) >> 8)
        self.__PushByte(value & 0xFF)

    def __PushDWord(self, value: int):
        self.__PushWord((value & 0xFFFF0000) >> 16)
        self.__PushWord(value & 0xFFFF)

    def __PopByte(self) -> int:
        self.ESP -= 1

        if self.ESP < self.EBP:
            self.RaiseInterrupt(self.StackUnderflow)

        return self.Memory[self.ESP]

    def __PopWord(self) -> int:
        return self.__PopByte() << 8 | self.__PopByte()

    def __PopDWord(self) -> int:
        return self.__PopWord() << 16 | self.__PopWord()

    def __ReadReg(self, code: int) -> int:
        if code == 0:
            return self.EAX

        elif code == 1:
            return self.EBX

        elif code == 2:
            return self.ECX

        elif code == 3:
            return self.EDX

        elif code == 4:
            return self.EDI

        elif code == 5:
            return self.ESI

        elif code == 6:
            return self.EBP

        elif code == 7:
            return self.ESP

    def __WriteReg(self, code: int, value: int, size: int):
        if size == 32:
            anded = 0

        elif size == 16:
            anded = 0xFFFF0000

        elif size == 8:
            anded = 0xFFFFFF00

        if code == 0:
            self.EAX = (self.EAX & anded) | value

        if code == 1:
            self.EBX = (self.EBX & anded) | value

        if code == 2:
            self.ECX = (self.ECX & anded) | value

        if code == 3:
            self.EDX = (self.EDX & anded) | value

        if code == 4:
            self.EDI = (self.EDI & anded) | value

        if code == 5:
            self.ESI = (self.ESI & anded) | value

        if code == 6:
            self.EBP = (self.EBP & anded) | value

        if code == 7:
            self.ESI = (self.ESI & anded) | value

    def __ReadByte(self, addr: int) -> int:
        return self.Memory[addr]

    def __ReadWord(self, addr: int) -> int:
        return self.__ReadByte(addr) << 8 | self.__ReadByte(addr+1)

    def __ReadDWord(self, addr: int) -> int:
        return self.__ReadWord(addr) << 16 | self.__ReadWord(addr+2)

    def __WriteByte(self, addr: int, value: int):
        self.Memory[addr] = value

    def __WriteWord(self, addr: int, value: int):
        self.__WriteByte(addr, (value & 0xFF00) >> 8)
        self.__WriteByte(addr+1, value & 0xFF)

    def __WriteDWord(self, addr: int, value: int):
        self.__WriteWord(addr, (value & 0xFFFF0000) >> 16)
        self.__WriteWord(addr+2, value & 0xFFFF)
