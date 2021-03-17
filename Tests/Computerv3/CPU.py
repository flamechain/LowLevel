'''
Contains instructions and ALU
'''

import re

from Memory import VirtualMemory
from Types import *

class CPU:

    PC = Byte(0) # Program Counter
    SP = 0 # Stack Pointer
    PS = 0 # Processor Status

    # FLAGS
    C = 0 # Carry
    Z = 0 # Zero
    N = 0 # Sign
    T = 0 # Trap
    O = 0 # Overflow
    B = 0 # Break
    I = 0 # Interupt Disable
    U = 1 # Unused

    # Registers
    A = 0b00000000
    EAX = 0b00000000
    EBX = 0b00000000
    ECX = 0b0000000000000000
    EDX = 0b0000000000000000

    def __init__(self, reset_vector=0xFF00, memory=VirtualMemory):
        self.U = 1
        self.UpdatePS()
        self.SP = 0x01FF
        self.cycles = 0
        self.out = [0b00000000, 0b00000000]
        self.memory = memory()
        self.memory.Data[0xFFFC] = (reset_vector & 0xFF00) >> 8
        self.memory.Data[0xFFFD] = (reset_vector & 0xFF)
        self.Reset()

    def LoadProgram(self, prg) -> None:
        prg = prg.replace('\n', '').replace(' ', '')
        prg = re.findall('........', prg)
        for i in range(len(prg)):
            self.memory.Data[i] = int(prg[i], 2)
        self.Reset()

    def Reset(self):
        self.PC = Byte((self.memory.Data[0xFFFC] << 8) | (self.memory.Data[0xFFFD]))

    def UpdatePS(self):
        self.PS = self.C << 7 | self.Z << 6 | self.N << 5 | self.T << 4 | self.O << 3 | self.B << 2 | self.I << 1 | self.U

    def UpdateFlags(self):
        self.C = self.PS & 0b10000000
        self.Z = self.PS & 0b01000000
        self.S = self.PS & 0b00100000
        self.T = self.PS & 0b00010000
        self.O = self.PS & 0b00001000
        self.B = self.PS & 0b00000100
        self.I = self.PS & 0b00000010
        self.U = self.PS & 0b00000001

    def FetchByte(self) -> Byte:
        '''Gets next byte in memory'''
        byte = self.memory.Data[self.PC.int()]
        self.PC += 1
        self.cycles -= 1

        return byte

    def FetchWord(self) -> Word:
        '''Gets next word in memory'''
        word = self.memory.Data[self.PC.int()] << 8
        self.PC += 1
        word = word | (self.memory.Data[self.PC.int()])
        self.PC += 1
        self.cycles -= 2

        return word

    def WriteByte(self, value: Byte, address: Word) -> None:
        '''Write a byte to memory'''
        self.memory.Data[address] = value
        self.cycles -= 1

        return self.memory

    def AddrAbsolute(self) -> Word:
        '''Absolute address mode'''
        return self.FetchWord()

    def SetFlags_ZN(self, value: Byte) -> None:
        '''Sets Zero and Negative flags'''
        self.Z = 1 if value == 0 else 0
        self.N = 1 if (value & 0b10000000) > 0 else 0
        self.UpdatePS()

    def NegByte(self, value: bytes) -> bytes:
        '''Converts bytes to negative form because Python dynamically typing screwed me over'''
        if (value & 0b10000000) and (value > 0):
            value -= 0x100

        return value

    def RORLogic(self, Value: Byte) -> Byte:
        '''Handles ROR logic'''
        Bit7 = self.C
        self.C = 1 if (Value & 0b1) > 0 else 0
        Value = (Value >> 1) & 0xFF
        Value = Value | (Bit7 << 7)
        self.SetFlags_ZN(Value)
        self.cycles -= 1

        return Value

    def SPToAddress(self) -> Word:
        '''Stack Pointer to word'''
        return 0x0100 | self.SP

    def PushPCToStack(self) -> None:
        '''Push Program Counter to stack'''
        self.WriteByte(self.PC.int() >> 8, self.SPToAddress())
        self.SP -= 1
        self.PC -= 1
        self.WriteByte(self.PC.int() & 0xFF, self.SPToAddress())
        self.SP -= 1

    def PopWordFromStack(self) -> Word:
        '''Pop word from stack'''
        Value = self.ReadWord(self.SPToAddress()+1)
        self.SP += 2
        self.cycles -= 1

        return Value

    def ReadWord(self, address: Word) -> Word:
        '''Reads a word from address'''
        LoByte = self.ReadByte(address)
        HiByte = self.ReadByte(address + 1)

        return LoByte | (HiByte << 8)

    def ReadByte(self, address: Word) -> Byte:
        '''Reads a byte from address'''
        data = self.memory.Data[address]
        self.cycles -= 1

        return data


    INS_NOP = 0x00
    INS_LDAC_IM = 0xE8
    INS_STAC_ABS = 0x31
    INS_JMP_ABS = 0xE0
    INS_ROR_AC = 0x1E
    INS_JSR = 0xE2
    INS_RSR = 0x23

    def Execute(self, cycles: int) -> int:
        GivenCycles = cycles
        self.cycles = cycles

        while self.cycles > 0:
            Ins = self.FetchByte()

            if self.T:
                input(f'Current Address: {self.PC.hex()}; Current Instruction: {hex(Ins)}')

            if Ins == self.INS_NOP:
                pass

            elif Ins == self.INS_LDAC_IM:
                self.A = self.FetchByte()
                self.SetFlags_ZN(self.A)

            elif Ins == self.INS_STAC_ABS:
                Address = self.AddrAbsolute()
                self.WriteByte(self.A, Address)

            elif Ins == self.INS_JMP_ABS:
                self.PC = Byte(self.FetchWord())

            elif Ins == self.INS_ROR_AC:
                self.A = self.RORLogic(self.A)

            elif Ins == self.INS_JSR:
                SubAddr = self.FetchWord()
                self.PushPCToStack()
                self.PC = Byte(SubAddr)
                self.cycles -= 1

            elif Ins == self.INS_RSR:
                ReturnAddress = self.PopWordFromStack()
                self.PC = Byte(ReturnAddress + 1)
                self.cycles -= 2

            else:
                raise Exception(f'Invalid opcode at {self.PC.hex()}: {hex(Ins)}')

        self.out = [self.memory.Data[0x6001] & self.memory.Data[0x6003], self.memory.Data[0x6000] & self.memory.Data[0x6002]]
        return GivenCycles - self.cycles
