class Memory:
    def __init__(self):
        self.Data = []
        for i in range(16):
            self.Data.append(0x00)

class Flags:
    def __init__(self):
        self.C = 0
        self.Z = 0
        self.S = 0
        self.U = 0

    def Full(self):
        return self.C << 3 | self.Z << 2 | self.S << 1 | self.U

class CPU:
    def __init__(self):
        self.PC = 0b0000
        self.PS = Flags()
        self.HPC = 0

        self.A = 0b00000000
        self.Data = Memory().Data
        self.cycles = 0

    def FetchNibble(self):
        byte = self.Data[self.PC]
        if self.HPC == 0:
            self.HPC = 1
            self.cycles -= 0.5
            return (byte & 0xF0) >> 4
        else:
            self.HPC = 0
            self.PC += 1
            self.cycles -= 0.5
            return byte & 0xF

    def WriteByte(self, addr, value):
        self.Data[addr] = value

    def ReadByte(self, addr):
        return self.Data[addr]

    def SetFlags(self, value):
        if value == 0:
            self.PS.Z = 1
        if value > 255:
            self.PS.C = 1
        if value < 0:
            self.PS.S = 1

    def WrapByte(self, value):
        return value & 0xFF

    def HandleInterupt(self, code):
        if code == 0b0000:
            print(chr(0b1100000 | self.A), end='')

    INS_NOP = 0x0
    INS_LDA = 0x1
    INS_ADD = 0x2
    INS_SUB = 0x3
    INS_STA = 0x4
    INS_LDI = 0x5
    INS_JMP = 0x6
    INS_JC  = 0x7
    INS_JZ  = 0x8
    INS_    = 0x9
    INS_    = 0xA
    INS_    = 0xB
    INS_    = 0xC
    INS_INT = 0xD
    INS_OUT = 0xE
    INS_HLT = 0xF

    def Execute(self, cycles=16):
        self.cycles = cycles

        while self.cycles > 0:
            Ins = self.FetchNibble()
            Value = self.FetchNibble()

            if Ins == self.INS_NOP:
                pass

            elif Ins == self.INS_LDA:
                self.A = self.ReadByte(Value)
                Insr = 'LDA'

            elif Ins == self.INS_ADD:
                self.A += Value
                self.SetFlags(self.A)
                self.A = self.WrapByte(self.A)
                Insr = 'ADD'

            elif Ins == self.INS_SUB:
                self.A -= Value
                self.SetFlags(self.A)
                self.A = self.WrapByte(self.A)
                Insr = 'SUB'

            elif Ins == self.INS_STA:
                self.WriteByte(Value, self.A)
                Insr = 'STA'

            elif Ins == self.INS_LDI:
                self.A = Value
                Insr = 'LDI'

            elif Ins == self.INS_JMP:
                self.PC = Value
                Insr = 'JMP'

            elif Ins == self.INS_JC:
                if self.PS.C == 1:
                    self.PC = Value
                Insr = 'JC'

            elif Ins == self.INS_JZ:
                if self.PS.Z == 1:
                    self.PC = Value
                Insr = 'JZ'

            elif Ins == self.INS_INT:
                self.HandleInterupt(Value)
                Insr = 'INT'

            elif Ins == self.INS_OUT:
                print(bin(self.A))
                Insr = 'OUT'

            elif Ins == self.INS_HLT:
                input("HLT > ")
                Insr = 'HLT'

            else:
                print("%s: Unhandled instruction: %s" % ('0'*(4-len('{0:b}'.format(self.PC)))+'{0:b}'.format(self.PC), bin(Ins << 4 | Value)))
                continue

            print("%s: %s %s" % ('0'*(4-len('{0:b}'.format(self.PC)))+'{0:b}'.format(self.PC), Insr, '0'*(4-len('{0:b}'.format(Value)))+'{0:b}'.format(Value)))
