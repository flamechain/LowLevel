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
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0

        self.SP = 0x0FFF
        self.PC = 0
        self.PS = Flags()

        self.Data = Memory(100).Data
        self.offset = [0, 0]

    def LoadProgram(self, prg):
        with open(prg, 'rb') as f:
            contents = re.findall('..', f.read().hex())

        for i in range(len(contents)):
            self.Data[i] = int(contents[i], 16)

        self.PC = 0

    def SetRegister(self, code, value):
        if code == 0:
            self.EAX = value
        elif code == 1:
            self.EBX = value
        elif code == 2:
            self.ECX = value
        elif code == 3:
            self.EDX = value
        elif code == 4:
            self.ESI = value
        elif code == 5:
            self.ESP = value
        elif code == 6:
            self.EDI = value
        elif code == 7:
            self.EBP = value
        elif code == 8:
            self.AX = value
        elif code == 9:
            self.BX = value
        elif code == 10:
            self.CX = value
        elif code == 11:
            self.DX = value

    def GetRegister(self, code):
        if code == 0:
            return self.EAX
        elif code == 1:
            return self.EBX
        elif code == 2:
            return self.ECX
        elif code == 3:
            return self.EDX
        elif code == 4:
            return self.ESI
        elif code == 5:
            return self.ESP
        elif code == 6:
            return self.EDI
        elif code == 7:
            return self.EBP
        elif code == 8:
            return self.AX
        elif code == 9:
            return self.BX
        elif code == 10:
            return self.CX
        elif code == 11:
            return self.DX

    def HandleInterupts(self, code):
        if code == 1:
            if self.EAX == 0:
                msg = self.EBX
                msg_len = self.ECX
                out = self.EDX
                counter = 0
                toprint = ''
                length = self.ReadByte(self.ECX)
                byte = self.ReadByte(self.EBX+counter)

                while length > 0:
                    toprint += chr(byte)
                    length -= 1
                    counter += 1

                print(toprint)

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
            Mod = self.FetchByte()
            param1 = self.FetchByte()
            param2 = self.FetchByte()
            param3 = self.FetchByte()
            try:
                string = 'Addr %s -> %s: %s, %s %s %s' % (hex(self.PC-5), decoder[Ins], hex(Mod), hex(param1), hex(param2), hex(param3))
                print(string)
            except:
                string = 'Addr %s -> %s: Unknown Instruction' % (hex(self.PC-5), hex(Ins))
                print(string)
                return

            if Ins == INS_HLT:
                return

            elif Ins == INS_MOV:
                if Mod == 0:
                    value = self.GetRegister(param2)
                    self.SetRegister(param1, value)

                elif Mod == 3:
                    value = param2 << 8 | param3
                    self.SetRegister(param1, value)

            elif Ins == INS_CALL:
                start = (param1 << 8 | param2) + self.EBP
                self.PushPCToStack()
                self.PC = start

            elif Ins == INS_INT:
                self.HandleInterupts(Mod)

            elif Ins == INS_RET:
                self.EBX = Mod
                self.PopPCFromStack()

            else:
                print("Unknown instruction at address %s: %s" % (hex(self.PC), hex(Ins)))
                return
