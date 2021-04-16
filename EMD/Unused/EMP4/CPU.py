import sys

def Memory(size=65536):
    data = []

    for i in range(size):
        data.append(0)

    return data

class Flags:
    def __init__(self):
        self.V = 0
        self.Z = 0
        self.U1 = 0
        self.U2 = 0

class CPU:
    def __init__(self, size):
        self.Data = Memory(size)
        self.size = size
        self.PC = 0
        self.PS = Flags()
        self.A = 0b0000
        self.B = 0b0000

    INS_HLT = 0x0
    INS_LDA = 0x1
    INS_LDB = 0x2
    INS_ADD = 0x3
    INS_SUB = 0x4
    INS_CMP = 0x5
    INS_JZ  = 0x6
    INS_OUT = 0x7
    INS_STA = 0x8
    INS_STB = 0x9
    INS_TRA = 0xA
    INS_TRB = 0xB

    def FetchNibble(self):
        if self.PC > self.size:
            print("Out of memory")
            sys.exit()

        value = self.Data[self.PC]
        self.PC += 1

        return value

    def SetFlags(self, value: int) -> None:
        if value == 0:
            self.PS.Z = 1

        if value > 15:
            self.PS.V = 1

    def ReadNibble(self, addr: int) -> int:
        return self.Data[addr]

    def WrapNibble(self, value: int) -> int:
        if value > 15:
            return 15

        return value

    def WriteNibble(self, value: int, addr: int) -> None:
        self.Data[addr] = value

    def Start(self):
        while True:
            Ins = self.FetchNibble()

            if Ins == self.INS_HLT:
                return

            elif Ins == self.INS_LDA:
                self.A = self.ReadNibble(self.FetchNibble())
                self.SetFlags(self.A)

            elif Ins == self.INS_LDB:
                self.B = self.ReadNibble(self.FetchNibble())
                self.SetFlags(self.B)

            elif Ins == self.INS_ADD:
                self.A += self.ReadNibble(self.FetchNibble())
                self.SetFlags(self.A)

            elif Ins == self.INS_SUB:
                self.A -= self.ReadNibble(self.FetchNibble())
                self.SetFlags(self.A)

            elif Ins == self.INS_CMP:
                Value = self.A - self.ReadNibble(self.FetchNibble())
                self.SetFlags(Value)

            elif Ins == self.INS_JZ:
                loc = self.FetchNibble()
                if self.PS.Z:
                    self.PC = loc

            elif Ins == self.INS_OUT:
                print(bin(self.A))

            elif Ins == self.INS_STA:
                self.WriteNibble(self.A, self.FetchNibble())

            elif Ins == self.INS_STB:
                self.WriteNibble(self.B, self.FetchNibble())

            elif Ins == self.INS_TRA:
                self.B = self.A

            elif Ins == self.INS_TRB:
                self.A = self.B

            else:
                print("%s: Unhandled Instruction: %s" % (bin(self.PC), bin(Ins)))
