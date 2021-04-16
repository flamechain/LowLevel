from instructions import *
import re
import msvcrt

class Memory:
    def __init__(self, size):
        self.Data = []
        for i in range(size):
            self.Data.append(0)

class Flags:
    def __init__(self):
        self.Z = 0
        self.C = 0
        self.V = 0
        self.S = 0
        self.B = 0
        self.T = 0
        self.U = 0
        self.I = 0

    def PS(self):
        return self.Z << 7 | self.C << 6 | self.V << 5 | self.S << 4 | self.B << 3 | self.T << 2 | self.U << 1 | self.I

class CPU:
    def __init__(self):
        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.ESI = 0
        self.ESP = 0
        self.EDI = 0
        self.EBP = 0

        self.ISF = 0
        self.ISS = 0
        self.MSR = 0
        self.FVR = 0
        self.SVR = 0

        self.PC = 0
        self.Stack = []

        self.Data = Memory(65536).Data # 16 ** 4

        self.PS = Flags()
        self.cycles = 0
        self.proc = []
        self.in_proc = False

    def LoadProgram(self, filename, location=0):
        '''Given a binary filename, loads the contents into RAM'''
        with open(filename, 'rb') as f:
            contents = f.read()
            contents = re.findall("..", contents.hex())
        
        enHiH = int(contents[0], 16) << 24
        enHiL = int(contents[1], 16) << 16
        enLoH = int(contents[2], 16) << 8
        enLoL = int(contents[3], 16)
        self.PC = enHiH | enHiL | enLoH | enLoL

        for i in range(len(contents)-4):
            if (len(self.Data)-1) < (i+location):
                self.Data.append(int(contents[i+4], 16))

            else:
                self.Data[i+location] = int(contents[i+4], 16)

    def Bootup(self):
        self.Execute('inf')

    def FetchByte(self):
        value = self.Data[self.PC]
        self.cycles -= 1
        self.PC += 1

        return value

    def FetchDWord(self):
        Hih = self.Data[self.PC] << 24
        Hio = self.Data[self.PC+1] << 16
        Loh = self.Data[self.PC+2] << 8
        Loo = self.Data[self.PC+3]
        self.PC += 4
        
        return Hih | Hio | Loh | Loo

    def SetRegister(self, code, value):
        if code == 0:
            self.EAX = value

    def EnterStack(self):
        self.in_proc = True
        self.Stack.append(self.PC)

    def ReturnFromStack(self):
        self.in_proc = False
        self.proc.pop()
        self.PC = self.Stack.pop() + 1
        if self.proc != []:
            self.in_proc = True

    def Execute(self, cycles):
        '''Execute, halting on cycles'''
        self.cycles = cycles

        if self.cycles == 'inf':
            self.cycles = 0

        while (self.cycles > 0) or (cycles == 'inf'):
            if self.in_proc:
                self.proc[-1] -= 1

                if self.proc[-1] == 0:
                    self.ReturnFromStack()

            self.ISF = self.FetchByte()

            if self.ISF not in [INS_BRK, INS_NOP]:
                self.ISS = self.FetchByte()

            if self.ISF == INS_HLT:
                return

            elif self.ISF == INS_MOV:
                if self.ISS & 0b11000000 == 0b01000000:
                    if self.ISS & 0b111 == 0b000:
                        value = self.FetchDWord()
                        self.SetRegister((self.ISS & 0b111000) >> 3, value)

            elif self.ISF == INS_CALL:
                self.proc.append(self.FetchByte())
                self.EnterStack()
                self.PC = self.ISS

            elif self.ISF == INS_INT:
                if self.ISS == 0xCC:
                    keypress = msvcrt.getch()
                    self.EDI = ord(keypress)
                elif self.ISS == 0xCD:
                    char = self.FetchByte()
                    while char != 0:
                        print(chr(char), end='')
                        char = self.FetchByte()
