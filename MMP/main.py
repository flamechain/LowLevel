import time

NOP = 0
LDA = 1
ADD = 2
OUT = 3
HLT = 4
SUB = 5
STA = 6
LDI = 7
JMP = 8
JC = 9
JZ = 10

class CPU:
    def __init__(self):
        self.RAM = []

        for i in range(256):
            self.RAM.append(0)

        self.A = 0
        self.B = 0

        self.hz = 5

        self.IP = 0
        self.CF = 0
        self.ZF = 0
        self.SF = 0

        self.Bus = 0

    def Fetch(self):
        self.Bus = self.RAM[self.IP]
        self.IP += 1

    def Read(self):
        self.Bus = self.RAM[self.Bus]

    def Decode(self):
        if self.Bus == NOP:
            self.NOP()

        elif self.Bus == LDA:
            self.LDA()

        elif self.Bus == ADD:
            self.ADD()

        elif self.Bus == OUT:
            self.OUT()

        elif self.Bus == HLT:
            self.HLT()

        elif self.Bus == SUB:
            self.SUB()

        elif self.Bus == STA:
            self.STA()

        elif self.Bus == LDI:
            self.LDI()

        elif self.Bus == JMP:
            self.JMP()

        elif self.Bus == JC:
            self.JC()

        elif self.Bus == JZ:
            self.JZ()

    def NOP(self):
        pass

    def LDA(self):
        self.Fetch()
        self.A = self.Bus

    def ADD(self):
        self.Fetch()
        res = self.A + self.Bus
        self.Bus = res & 0xFF

        if res & 0b100000000:
            self.CF = 1
        else:
            self.CF = 0

        if res & 0b10000000:
            self.SF = 1
        else:
            self.SF = 0

        if res == 0:
            self.ZF = 1
        else:
            self.ZF = 0

        self.A = self.Bus

    def OUT(self):
        self.Bus = self.A
        print(self.Bus)

    def HLT(self):
        input('HLT: ')

    def SUB(self):
        self.Fetch()
        res = self.A - self.Bus
        self.Bus = res & 0xFF

        if res & 0b10000000:
            self.SF = 1
        else:
            self.SF = 0

        if res == 0:
            self.ZF = 1
        else:
            self.ZF = 0

        self.A = self.Bus

    def STA(self):
        self.Fetch()

    def LDI(self):
        pass

    def JMP(self):
        self.Fetch()
        self.IP = self.Bus

    def JC(self):
        self.Fetch()

        if self.CF:
            self.IP = self.Bus

    def JZ(self):
        self.Fetch()

        if self.ZF:
            self.IP = self.Bus

    def Loop(self):
        while True:
            start = time.time()
            self.Fetch()
            self.Decode()
            sleep = 1/self.hz - (time.time() - start)

            if sleep < 0:
                print('Clock speed too slow')
                continue

            time.sleep(sleep)

cpu = CPU()

code = [
    OUT,        # 0
    ADD, 15,    # 1, 2
    JC, 7,      # 3, 4
    JMP, 0,     # 5, 6
    SUB, 15,    # 7, 8
    OUT,        # 9
    JZ, 0,      # 10, 11
    JMP, 7      # 12, 13
]

cpu.RAM[0:len(code)] = code
cpu.hz = 800

cpu.Loop()
