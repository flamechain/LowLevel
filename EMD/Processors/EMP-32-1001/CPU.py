from Instructions import *
import re
import sys
import msvcrt

class Memory:
    def __init__(self, size):
        self.Data = []

        for i in range(size):
            self.Data.append(0x0)

class Flags:
    def __init__(self):
        self.Z = 0
        self.C = 0
        self.S = 0
        self.V = 0
        self.B = 0
        self.U = 0
        self.T = 0
        self.I = 0

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

        self.SP = 0x0FFF
        self.PC = 0
        self.PS = Flags()

        self.Data = Memory(10000).Data
        self.offset = [0, 0]

    def LoadProgram(self, prg):
        with open(prg, 'rb') as f:
            contents = re.findall('..', f.read().hex())

        for i in range(len(contents)):
            self.Data[i] = int(contents[i], 16)

        self.PC = 0

    def SetRegister(self, code, value, size=32):
        if size == 32:
            if code == 0:
                self.EAX = value
            elif code == 1:
                self.EBX = value
            elif code == 2:
                self.ECX = value
            elif code == 3:
                self.EDX = value
            elif code == 7:
                self.EBP = value
        elif size == 8:
            if code == 3:
                self.EDX = (self.EDX & 0xFFFFFF00) | value
            elif code == 4:
                self.EDX = (self.EDX & 0xFFFF00FF) | (value << 8)

    def GetRegister(self, code):
        if code == 0:
            return self.EAX

    def HandleInterupts(self, code):
        if code == 0:
            sys.exit()

        elif code == 1:
            self.EAX = ord(msvcrt.getch())

        elif code == 2:
            toprint = self.ReadByte(self.EDX)
            counter = 0
            while toprint != 0:
                print(chr(toprint), end='')
                toprint = self.ReadByte(self.EDX + counter)
                counter += 1

        elif code == 3:
            y = (self.EDX & 0xFF00) >> 8
            if self.offset[1] < y:
                print('\n'*(y-self.offset[1]), end='')
            else:
                print('\n'*y, end='')
            x = self.EDX & 0xFF
            if self.offset[0] < x:
                print(' '*(x-self.offset[0]), end='')
            else:
                print(' '*x, end='')
            self.offset = [x, y]

        elif code == 4:
            print(chr(self.EAX & 0xFF), end='')

        elif code == 5:
            text = ''
            char = self.ReadByte(self.ECX + self.EBP)
            counter = 0
            while char != 0:
                text += chr(char)
                char = self.ReadByte(self.EDX + self.EBP + counter)
                counter += 1

            import tkinter as tk
            root = tk.Tk()
            T = tk.Text(root, height=2, width=30)
            T.pack()
            T.insert(tk.END, text)
            tk.mainloop()

    def ReadByte(self, address):
        return self.Data[address]

    def ReadDWord(self, address):
        HiH = self.Data[address] << 24
        HiL = self.Data[address+1] << 16
        LoH = self.Data[address+2] << 8
        LoL = self.Data[address+3]

        return HiH | HiL | LoH | LoL

    def FetchByte(self):
        value = self.Data[self.PC]
        self.PC += 1

        return value

    def FetchDWord(self):
        Hih = self.Data[self.PC] << 24
        Hio = self.Data[self.PC+1] << 16
        Loh = self.Data[self.PC+2] << 8
        Loo = self.Data[self.PC+3]
        self.PC += 4
        
        return Hih | Hio | Loh | Loo

    def FetchWord(self):
        Hi = self.Data[self.PC] << 8
        Lo = self.Data[self.PC+1]
        self.PC += 2

        return Hi | Lo

    def WriteDWord(self, value, address):
        self.Data[address] = (value & 0xFF000000) >> 24
        self.Data[address+1] = (value & 0xFF0000) >> 16
        self.Data[address+2] = (value & 0xFF00) >> 8
        self.Data[address+3] = value & 0xFF

    def WriteByte(self, value, address):
        self.Data[address] = value

    def PushPCToStack(self):
        self.WriteDWord(self.PC, self.SP-4)
        self.SP -= 4

    def PopPCFromStack(self):
        self.PC = self.ReadDWord(self.SP)
        self.SP += 4

    def Boot(self):
        while True:
            Ins = self.FetchByte()

            if Ins not in [INS_HLT, INS_CALL, INS_JMP, INS_JE, INS_INC, INS_DEC]:
                Mod = self.FetchByte()

            if Ins == INS_HLT:
                return

            elif Ins == INS_MOV:
                size = 32
                if (Mod & 0b11000000) >> 6 == 1:
                    if Mod & 0b111 == 0:
                        value = self.FetchDWord()
    
                    elif Mod & 0b111 == 1:
                        value = self.FetchDWord() + self.EBP
                    
                    elif Mod & 0b111 == 0b111:
                        addr = self.FetchDWord() + self.EBP
                        value = self.ReadByte(addr)
                        size = 8

                    self.SetRegister((Mod & 0b111000) >> 3, value, size)

                elif (Mod & 0b11000000) >> 6 == 2:
                    if Mod & 0b111000 == 0b011000:
                        src = self.FetchDWord()

                    self.WriteByte(self.GetRegister(Mod & 0b111), src + self.EBP)

            elif Ins == INS_CALL:
                start = self.FetchDWord() + self.EBP
                self.PushPCToStack()
                self.PC = start

            elif Ins == INS_INT:
                self.HandleInterupts(Mod)

            elif Ins == INS_RET:
                self.EBX = Mod
                self.PopPCFromStack()

            elif Ins == INS_JMP:
                self.PC = self.FetchDWord()

            elif Ins == INS_CMP:
                if Mod & 0b11000000 == 0b11000000:
                    if Mod & 0b111000 == 0b100000:
                        addr = self.FetchDWord() + self.EBP
                        value1 = self.ReadByte(addr)
                    if Mod & 0b111 == 0b000:
                        value2 = self.FetchDWord()
                
                res = value1 - value2

                if res < 0:
                    self.PS.S = 1

                if res == 0:
                    self.PS.Z = 1

            elif Ins == INS_JE:
                addr = self.FetchDWord() + self.EBP
                if self.PS.Z == 1:
                    self.PC = addr

            elif Ins == INS_INC:
                addr = self.FetchDWord() + self.EBP
                value = self.ReadByte(addr)
                value += 1
                self.WriteByte(value, addr)

            elif Ins == INS_DEC:
                addr = self.FetchDWord() + self.EBP
                value = self.ReadByte(addr)
                value -= 1
                self.WriteByte(value, addr)

            else:
                print("Unknown instruction at address %s: %s" % (hex(self.PC), hex(Ins)))
                return
