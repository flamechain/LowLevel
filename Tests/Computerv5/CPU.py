from VirtualRAM import Memory
from Instructions import *

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

    def __init__(self, memory: Memory, rVector=0x00008000, irqVector=0x00000006, nmiVector=0x00000006):
        # Vectors
        self.Data = memory.Data
        self.Data[0x00000000] = rVector & 0xFFFF0000 >> 16
        self.Data[0x00000001] = rVector & 0x0000FFFF
        self.Data[0x00000002] = irqVector & 0xFFFF0000 >> 16
        self.Data[0x00000003] = irqVector & 0x0000FFFF
        self.Data[0x00000004] = nmiVector & 0xFFFF0000 >> 16
        self.Data[0x00000005] = nmiVector & 0x0000FFFF

        # Registers
        self.EAX = 0x00000000
        self.EDX = 0x00000000
        self.ECX = 0x00000000
        self.EBX = 0x00000000
        self.EBP = 0x00000000
        self.EDI = 0x00000000
        self.ESI = 0x00000000
        self.ESP = 0x00000000
        self.AX = self.EAX & 0xFFFF
        self.DX = self.EDX & 0xFFFF
        self.CX = self.ECX & 0xFFFF
        self.BX = self.EBX & 0xFFFF
        self.BP = self.EBP & 0xFFFF
        self.DI = self.EDI & 0xFFFF
        self.SI = self.ESI & 0xFFFF
        self.SP = self.ESP & 0xFFFF
        self.AH = self.AX & 0xFF00 >> 8
        self.DH = self.DX & 0xFF00 >> 8
        self.CH = self.CX & 0xFF00 >> 8
        self.BH = self.BX & 0xFF00 >> 8
        self.AL = self.AX & 0xFF
        self.DL = self.DX & 0xFF
        self.CL = self.CX & 0xFF
        self.BL = self.BX & 0xFF

        # Proccesor State
        self.PC = rVector
        self.SP = 0xFFFF
        self.PS = Flags()

        self.cycles = 0
        self.bitsize = 8

    def UpdateRegisters(self, changed=32):
        '''Updates registers based on which registers where changed. This is because the registers are linked like in the real 8086.
           changed is an int that is either 32, 16, or 8 depending on which register was modified. This function is automatically run after instructions.'''
        if changed == 32:
            self.AX = self.EAX & 0xFFFF
            self.DX = self.EDX & 0xFFFF
            self.CX = self.ECX & 0xFFFF
            self.BX = self.EBX & 0xFFFF
            self.BP = self.EBP & 0xFFFF
            self.DI = self.EDI & 0xFFFF
            self.SI = self.ESI & 0xFFFF
            self.SP = self.ESP & 0xFFFF
            self.AH = self.AX & 0xFF00 >> 8
            self.DH = self.DX & 0xFF00 >> 8
            self.CH = self.CX & 0xFF00 >> 8
            self.BH = self.BX & 0xFF00 >> 8
            self.AL = self.AX & 0xFF
            self.DL = self.DX & 0xFF
            self.CL = self.CX & 0xFF
            self.BL = self.BX & 0xFF
        elif changed == 16:
            self.EAX = (self.EAX & 0xFFFF0000) | self.AX
            self.EDX = (self.EDX & 0xFFFF0000) | self.DX
            self.ECX = (self.ECX & 0xFFFF0000) | self.CX
            self.EBX = (self.EBX & 0xFFFF0000) | self.BX
            self.EBP = (self.EBP & 0xFFFF0000) | self.BP
            self.EDI = (self.EDI & 0xFFFF0000) | self.DI
            self.ESI = (self.ESI & 0xFFFF0000) | self.SI
            self.ESP = (self.ESP & 0xFFFF0000) | self.SP
            self.AH = self.AX & 0xFF00 >> 8
            self.DH = self.DX & 0xFF00 >> 8
            self.CH = self.CX & 0xFF00 >> 8
            self.BH = self.BX & 0xFF00 >> 8
            self.AL = self.AX & 0xFF
            self.DL = self.DX & 0xFF
            self.CL = self.CX & 0xFF
            self.BL = self.BX & 0xFF
        elif changed == 8: # Works on hi and lo
            self.AX = self.AH << 8 | self.AL
            self.DX = self.DH << 8 | self.DL
            self.CX = self.CH << 8 | self.CL
            self.BX = self.BH << 8 | self.BL
            self.EAX = (self.EAX & 0xFFFF0000) | self.AX
            self.EDX = (self.EDX & 0xFFFF0000) | self.DX
            self.ECX = (self.ECX & 0xFFFF0000) | self.CX
            self.EBX = (self.EBX & 0xFFFF0000) | self.BX
            self.EBP = (self.EBP & 0xFFFF0000) | self.BP
            self.EDI = (self.EDI & 0xFFFF0000) | self.DI
            self.ESI = (self.ESI & 0xFFFF0000) | self.SI
            self.ESP = (self.ESP & 0xFFFF0000) | self.SP

    def __set_reg32(self, code, value):
        '''Sets 32 bit register based on register code'''
        if code == 0:
            self.EAX = value
        elif code == 1:
            self.ECX = value
        elif code == 2:
            self.EDX = value
        elif code == 3:
            self.EBX = value
        elif code == 4:
            self.ESP = value
        elif code == 5:
            self.EBP = value
        elif code == 6:
            self.ESI = value
        elif code == 7:
            self.EDI = value

    def __set_reg16(self, code, value):
        '''Sets 16 bit register based on register code'''
        if code == 0:
            self.AX = value
        elif code == 1:
            self.CX = value
        elif code == 2:
            self.DX = value
        elif code == 3:
            self.BX = value
        elif code == 4:
            self.SP = value
        elif code == 5:
            self.BP = value
        elif code == 6:
            self.SI = value
        elif code == 7:
            self.DI = value

    def __set_reg8(self, code, value):
        '''Sets 8 bit register based on register code'''
        if code == 0:
            self.AL = value
        elif code == 1:
            self.CL = value
        elif code == 2:
            self.DL = value
        elif code == 3:
            self.BL = value
        elif code == 4:
            self.AH = value
        elif code == 5:
            self.CH = value
        elif code == 6:
            self.DH = value
        elif code == 7:
            self.BH = value

    def set_reg(self, code, value, size):
        '''Sets register based on register code'''
        if size == 0:
            self.set_reg8(code, value)
        else:
            self.set_reg32(code, value)

    def __get_reg32(self, code):
        '''Gets 32 bit register based on register code'''
        registers = {
            0: self.EAX,
            1: self.ECX,
            2: self.EDX,
            3: self.EBX,
            4: self.ESP,
            5: self.EBP,
            6: self.ESI,
            7: self.EDI
        }
        return registers[code]
    
    def __get_reg16(self, code):
        '''Gets 16 bit register based on register code'''
        registers = {
            0: self.AX,
            1: self.CX,
            2: self.DX,
            3: self.BX,
            4: self.SP,
            5: self.BP,
            6: self.SI,
            7: self.DI
        }
        return registers[code]

    def __get_reg8(self, code):
        '''Gets 8 bit register based on register code'''
        registers = {
            0: self.AL,
            1: self.CL,
            2: self.DL,
            3: self.BL,
            4: self.AH,
            5: self.CH,
            6: self.DH,
            7: self.BH
        }
        return registers[code]

    def __get_reg(self, code, size):
        '''Gets register value based on register code'''
        if size == 0:
            return self.get_reg8(code)
        else:
            return self.get_reg32(code)

    def __FetchByte(self) -> int:
        '''Gets next byte in memory, and increments program counter'''
        value = self.Data[self.PC]
        self.PC += 1
        self.cycles -= 1
        return value

    def __FetchDWord(self) -> int:
        '''Gets the next 4 bytes as double word, and increments the program counter'''
        return self.FetchByte() << 24 | self.FetchByte() << 16 | self.FetchByte() << 8 | self.FetchByte()

    def __INS_ADD(self, Ins, Mod):
        '''Adds values, acording to the 2 opcode bytes (Ins and Mod)'''
        mode = Ins & 0b1
        reg = self.get_reg((Mod & 0b111000) >> 3, mode)
        typ = Mod & 0b11000000

        if typ == 0b11000000:
            rm = self.get_reg(Mod & 0b111, mode)

        elif typ == 0:

            if Mod & 0b111 != 0b100:
                if Mod & 0b111 == 0b101:
                    rm = self.FetchDWord()

            else:
                SIB = self.FetchByte()

                multipliers = {
                    0: 1,
                    1: 2,
                    2: 4,
                    3: 8
                }

                rm = self.get_reg((SIB & 0b111000) >> 3, mode) * multipliers[(SIB & 0b11000000) >> 6]

                if SIB & 0b111 == 0b101:
                    rm += self.FetchDWord()

                else:
                    rm += self.get_reg(SIB & 0b111, mode)

        elif typ >> 6 == 1:
            if Mod & 0b111 != 0b100:
                if mode == 1:
                    rm = self.FetchByte() + self.get_reg32(Mod & 0b111)

        elif typ >> 6 == 2:
            if Mod & 0b111 != 0b100:
                if mode == 1:
                    rm = self.FetchDWord() + self.get_reg32(Mod & 0b111)

        if Ins & 0b10 == 0:
            dest = Mod & 0b111

        else:
            dest = (Mod & 0b111000) >> 3

        self.set_reg(dest, reg + rm, mode)

        if mode == 0:
            changed = 8

        else:
            changed = 32

        self.UpdateRegisters(changed)

    def Execute(self, cycles: int) -> int:
        '''Executes instructions limited on cycles. Cycles are consumed whenever the program couter is incremented. cycles == addresses'''
        self.cycles = cycles

        while self.cycles > 0:
            Ins = self.FetchByte()
            Mod = self.FetchByte()

            if Ins & 0b11111100 == INS_ADD:
                self.ADD_INS(Ins, Mod)

        return cycles - self.cycles
