class Memory:
    Data = []

    def __init__(self, size):
        for i in range(size):
            self.Data.append(0)

class Flags:
    def __init__(self):
        self.Z = 0
        self.V = 0

class CPU:
    def __init__(self):
        self.Data = Memory(4).Data
        self.A = 0
        self.PC = 0
        self.PS = Flags()

    INS_ADD = 0b00
    INS_JZ = 0b01
    INS_LDA = 0b10
    INS_STA = 0b11

    def Fetch(self):
        value = self.Data[self.PC]
        self.PC += 1
        return value

    def Read(self, addr):
        return self.Data[addr]

    def Write(self, value, addr):
        self.Data[addr] = value

    def Start(self):
        counter = len(self.Data) - 1
        while counter > 0:
            counter -= 1
            Ins = self.Fetch()
            
            if Ins == self.INS_ADD:
                self.A += self.Read(self.Fetch())
            elif Ins == self.INS_JZ:
                if self.PS.Z:
                    self.PC = self.Fetch()
            elif Ins == self.INS_LDA:
                self.A = self.Read(self.Fetch())
            elif Ins == self.INS_STA:
                self.Write(self.A, self.Fetch())

            print(self.A)
