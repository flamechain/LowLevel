class Memory:
    def __init__(self, size=2**16):
        '''### Memory object which contains an array of @param: size

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

        self.Data = []

        for i in range(size):
            self.Data.append(0)


class FLAGS:
    def __init__(self):
        self.CF = 0
        self.ZF = 0
        self.SF = 0
        self.TF = 0
        self.IF = 0
        self.OF = 0
        self.ID = 0
        self.RF = 0

    def full(self):
        return self.RF << 7 | self.ID << 6 | self.OF << 5 | self.IF << 4 | self.TF << 3 | self.SF << 2 | self.ZF << 1 | self.CF
