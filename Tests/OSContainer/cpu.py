class Memory:
    def __init__(self):
        self.Data = []
        for i in range(16 ** 5):
            self.Data.append(0x0)

class Flags:
    def __init__(self):
        self.C = 0
        self.Z = 0
        self.B = 0
        self.I = 0
        self.U = 0
        self.O = 0
        self.S = 0
        self.T = 0

    def PC(self):
        return self.C << 7 | self.Z << 6 | self.B << 5 | self.I << 4 | self.U << 3 | self.O << 2 | self.S << 1 | self.T

class CPU:
    def __init__(self):
        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.ESI = 0
        self.EDI = 0
        self.ESP = 0
        self.EBP = 0

        self.Data = Memory().Data

        self.PC = 0
        self.SP = 0
        self.PS = Flags()

    def FetchByte(self):
        value = self.Data[self.PC]
        self.PC += 1
        self.cycles -= 1
        return value

    def FetchDWord(self):
        Hih = self.Data[self.PC]
        self.PC += 1
        Hio = self.Data[self.PC]
        self.PC += 1
        Loh = self.Data[self.PC]
        self.PC += 1
        Loo = self.Data[self.PC]
        self.PC += 1
        self.cycles -= 4
        return (Hih << 24) | (Hio << 16) | (Loh << 8) | Loo

    def WriteDWord(self, res, src):
        self.Data[res] = (src & 0xFF000000) >> 24
        self.Data[res+1] = (src & 0xFF0000) >> 16
        self.Data[res+2] = (src & 0xFF00) >> 8
        self.Data[res+3] = src & 0xFF

    def ReadDWord(self, addr):
        Hih = self.Data[addr]
        Hio = self.Data[addr+1]
        Loh = self.Data[addr+2]
        Loo = self.Data[addr+3]
        return (Hih << 24) | (Hio << 16) | (Loh << 8) | Loo

    def LoadProgram(self, prg):
        loc = (int(prg[0], 16) << 24) | (int(prg[1], 16) << 16) | (int(prg[2], 16) << 8) | int(prg[3], 16)
        self.PC = loc
        for i in range(len(prg)):
            self.Data[i+loc] = int(prg[i], 16)

    INS_HLT = 0x1
    INS_MOV = 0x2

    def Execute(self, cycles='inf'):
        self.cycles = cycles
        if self.cycles == 'inf':
            self.cycles = 0

        while (self.cycles > 0) or (cycles == 'inf'):
            Ins = self.FetchByte()

            if Ins == self.INS_HLT:
                return

            elif Ins == self.INS_MOV:
                Mod = self.FetchByte()
                if Mod & 0b11000000 == 0b11000000:
                    if Mod & 0b111000 == 0b010000:
                        res = self.FetchDWord()
                    if Mod & 0b111 == 0b010:
                        src = self.FetchDWord()
                    self.WriteDWord(res, src)

            visual = self.ReadDWord(0xb8000)
            visual = hex(visual)[2:]
            char = '2f'
            if visual[:2] == char:
                print(chr(int(visual[2:4], 16)), end='')
            if visual[4:6] == char:
                print(chr(int(visual[6:8], 16)), end='')
