from termcolor import colored
import sys

class Mem:
    '''Virtual memory (Virtual RAM) object'''
    def __init__(self):
        self.MAX_MEM = 1024 * 64
        self.Data = []

    def Initilize(self) -> None:
        '''Fills memory with 0x00'''
        for i in range(self.MAX_MEM):
            try:
                self.Data[i] = 0

            except:
                self.Data.append(0)

class CPU:
    '''6502 CPU Emulator'''
    # Registers

    PC = None # Program Counter
    SP = None # Stack Pointer

    # General Purpose
    A = None
    X = None
    Y = None

    # Status Flags
    C = 1 # Carry
    Z = 1 # Zero
    I = 1 # Interupt Disable
    D = 1 # Decimal Mode
    B = 1 # Break Command
    Unused = 1 # Logical 1 all time, does nothing
    V = 1 # Overflow
    N = 1 # Negative

    PSL = [C, Z, I, D, B, Unused, V, N]
    PS = 0x00

    cycles = 0


    def Reset(self, memory: Mem, vector=0xFFFC) -> None:
        '''Resets Program Counter, Stack Pointer, and registers'''
        self.PC = vector
        self.SP = 0xFF

        self.D = 0

        self.A = 0
        self.X = 0
        self.Y = 0

        self.C = self.Z = self.I = self.B = self.V = self.N = 0
        self.Unused = 1
        self.PSL = [self.C, self.Z, self.I, self.D, self.B, self.Unused, self.V, self.N]
        self.PSLToPS()

        memory.Initilize()

    def LoadProgram(self, program: list, mem: Mem) -> bytes:
        '''Loads program into virtual memory (mem)'''
        At = -1
        LoadAddress = program[At+1] | (program[At+2] << 8)
        At += 2
        i = LoadAddress

        while i < (LoadAddress+len(program)-2):
            mem.Data[i] = program[At+1]
            At += 1
            i += 1

        return LoadAddress

    def PrintStatus(self) -> None:
        '''Prints registers and Processor Status'''
        print('A: %s X: %s Y: %s' % (self.A, self.X, self.Y))
        print('PC: %s SP: %s' % (self.PC, self.SP))
        binary = [str(i) for i in self.PSL]
        binary = ''.join(binary)
        print('PS: %s' % (str(self.N)+str(self.V)+str(self.Unused)+str(self.B)+str(self.D)+str(self.I)+str(self.Z)+str(self.C)))


    def WriteWord(self, data: bytes, address: bytes, memory: Mem) -> Mem:
        '''Writes a word'''
        memory.Data[address] = data & 0xFF
        memory.Data[address + 1] = data >> 8
        self.cycles -= 2

        return memory

    def WriteByte(self, data: bytes, address: bytes, memory: Mem) -> Mem:
        '''Writes a byte'''
        memory.Data[address] = data
        self.cycles -= 1

        return memory

    def FetchByte(self, memory: Mem) -> bytes:
        '''Gets a byte from memory'''
        data = memory.Data[self.PC]
        self.PC += 1
        self.CheckPC()
        self.cycles -= 1

        return data

    def FetchWord(self, memory: Mem) -> bytes:
        '''Gets a word from memory, little endian'''
        Data = memory.Data[self.PC]
        self.PC += 1
        self.CheckPC()
        Data = Data | (memory.Data[self.PC] << 8)
        self.PC += 1
        self.CheckPC()
        self.cycles -= 2

        return Data

    def ReadByte(self, address: bytes, memory: Mem) -> bytes:
        '''Reads a byte from address'''
        data = memory.Data[address]
        self.cycles -= 1

        return data

    def ReadWord(self, address: bytes, memory: Mem) -> bytes:
        '''Reads a word from address'''
        LoByte = self.ReadByte(address, memory)
        HiByte = self.ReadByte(address + 1, memory)

        return LoByte | (HiByte << 8)

    def CheckPC(self) -> None:
        '''Wrap Program Counter'''
        if self.PC > 0xFFFF:
            self.PC = 0x0000

    def AddrAbsolute(self, memory: Mem) -> bytes:
        '''Absolute Address mode'''
        return self.FetchWord(memory)

    def AddrZeroPage(self, memory: Mem) -> bytes:
        '''ZeroPage Address mode'''
        return self.FetchByte(memory)

    def AddrZeroPageXY(self, memory: Mem, register: bytes) -> bytes:
        '''ZeroPageX/Y Address mode'''
        address = self.FetchByte(memory) + register
        self.cycles -= 1
        return self.WrapAddress(address)

    def AddrAbsoluteXY(self, memory: Mem, register: bytes, sta=False) -> bytes:
        '''AbsoluteX/Y Address mode'''
        AbsoluteAddress = self.FetchWord(memory)
        AbsoluteAddressX = AbsoluteAddress + register

        if ((AbsoluteAddressX - AbsoluteAddress) >= 0xFF) or sta:
            self.cycles -= 1

        return AbsoluteAddressX

    def WrapAddress(self, address: bytes) -> bytes:
        '''Wrap address because Python doesn't do this automatically'''
        if str(hex(address))[-3] == '1':
            copy = str(hex(address))
            copy = [i for i in copy]
            copy[-3] = '0'
            copy = ''.join(copy)
            address = int(copy, 16)
        return address

    def SetZNFlags(self, register: bytes) -> None:
        '''Sets Zero and Negative flag status'''
        self.Z = 1 if register == 0 else 0
        self.N = 1 if (register & 0b10000000) > 0 else 0
        self.PSL[1] = self.Z
        self.PSL[-1] = self.N
        self.PSLToPS()

    def AddrInderectX(self, memory: Mem) -> bytes:
        '''InderectX Address mode'''
        ZeroPageAddress = self.FetchByte(memory)
        ZeroPageAddress += self.X
        self.cycles -= 1
        EffectiveAddress = self.ReadWord(ZeroPageAddress, memory)

        return EffectiveAddress

    def AddrInderectY(self, memory: Mem, sta=False) -> bytes:
        '''InderectY Address mode'''
        ZeroPageAddress = self.FetchByte(memory)
        EffectiveAddress = self.ReadWord(ZeroPageAddress, memory)
        EffectiveAddressY = EffectiveAddress + self.Y

        if ((EffectiveAddressY - EffectiveAddress) >= 0xFF) or sta:
            self.cycles -= 1
        
        return EffectiveAddressY

    def SPToAddress(self) -> bytes:
        '''Stack Pointer to word'''
        return 0x0100 | self.SP

    def PushPCToStack(self, memory: Mem) -> Mem:
        '''Push Program Counter to stack'''
        memory = self.WriteByte(self.PC >> 8, self.SPToAddress(), memory)
        self.SP -= 1
        self.PC -= 1
        memory = self.WriteByte(self.PC & 0xFF, self.SPToAddress(), memory)
        self.SP -= 1

        return memory

    def PushWordToStack(self, data: bytes, memory: Mem) -> Mem:
        '''Push word to stack'''
        memory = self.WriteByte(data >> 8, self.SPToAddress(), memory)
        self.SP -= 1
        memory = self.WriteByte(data & 0xFF, self.SPToAddress(), memory)
        self.SP -= 1
        return memory

    def PopWordFromStack(self, memory: Mem) -> bytes:
        '''Pop word from stack'''
        Value = self.ReadWord(self.SPToAddress()+1, memory)
        self.SP += 2
        self.cycles -= 1
        return Value

    def PushByteToStack(self, value: bytes, memory: Mem) -> Mem:
        '''Push byte to stack'''
        memory.Data[self.SPToAddress()] = value
        self.cycles -= 1
        self.SP -= 1
        self.cycles -=1

        return memory

    def PSLToPS(self) -> None:
        '''Convert Processor Status List to Processor Status byte'''
        binary = [str(i) for i in self.PSL]
        binary = ''.join(binary)
        binary = int(binary, 2)
        self.PS = int(str(hex(binary)), 16)

    def PSToPSL(self) -> None:
        '''Convert Processor Status byte to Processor Status List'''
        binary = '{0:b}'.format(self.PS)
        while len(binary) < 8:
            binary = '0' + binary
        self.PSL = [i for i in binary]

    def UpdatePS(self) -> None:
        '''Update Processor Status'''
        self.PSL[0] = self.N
        self.PSL[1] = self.V
        self.PSL[2] = self.Unused
        self.PSL[3] = self.B
        self.PSL[4] = self.D
        self.PSL[5] = self.I
        self.PSL[6] = self.Z
        self.PSL[7] = self.C
        self.PSLToPS()

    def UpdateFlags(self) -> None:
        '''Update flags'''
        self.N = int(self.PSL[0])
        self.V = int(self.PSL[1])
        self.Unused = int(self.PSL[2])
        self.B = int(self.PSL[3])
        self.D = int(self.PSL[4])
        self.I = int(self.PSL[5])
        self.Z = int(self.PSL[6])
        self.C = int(self.PSL[7])


    def PopByteFromStack(self, memory: Mem) -> bytes:
        '''Pop byte from stack'''
        self.SP += 1
        self.cycles -= 1
        SPWord = self.SPToAddress()
        Value = memory.Data[SPWord]
        self.cycles -= 1
        return Value

    def ANDRegister(self, address: bytes, memory: Mem) -> None:
        '''AND Register code'''
        self.A = self.A & self.ReadByte(address, memory)
        self.SetZNFlags(self.A)

    def EORRegister(self, address: bytes, memory: Mem) -> None:
        '''EOR Register code'''
        self.A = self.A ^ self.ReadByte(address, memory)
        self.SetZNFlags(self.A)

    def ORARegister(self, address: bytes, memory: Mem) -> None:
        '''ORA Register code'''
        self.A = self.A | self.ReadByte(address, memory)
        self.SetZNFlags(self.A)

    def ToBin(self, data: bytes, length: int) -> str:
        data = '{0:b}'.format(data)
        while len(data) < length:
            data = '0' + data
        return data

    def BITTest(self, address: bytes, memory: Mem) -> None:
        '''BIT test code'''
        Value = self.A & self.ReadByte(address, memory)
        self.Z = 1 if Value == 0 else 0
        self.N = 1 if (Value & 0b10000000) != 0 else 0
        self.V = 1 if (Value & 0b01000000) != 0 else 0
        self.UpdatePS()

    def WrapByte(self, value: bytes) -> bytes:
        '''Wrap byte because Python doesn't do this automatically'''
        if value > 0xFF:
            value = 0x00
        elif value < 0x00:
            value = 0xFF
        return value

    def WrapWord(self, value: bytes) -> bytes:
        '''Wrap word because Python doesn't do this automatically'''
        if value > 0xFFFF:
            value = 0x0000
        elif value < 0x0000:
            value = 0xFFFF
        return value

    def SignByte(self, value: bytes) -> bytes:
        '''Converts hex to negative because Python doesnt have static types'''
        if value > 128:
            value -= 0x100

        return value

    def NegByte(self, value: bytes) -> bytes:
        '''Converts bytes to negative form because Python dynamically typing screwed me over'''
        if (value & 0b10000000) and (value > 0):
            value -= 0x100

        return value

    def BranchIf(self, Value: bytes, Register: bytes, memory: Mem) -> None:
        '''Branch if Value == Register'''
        Offset = self.FetchByte(memory)
        Offset = self.SignByte(Offset)

        if (Value == Register):
            OldPC = self.PC
            self.PC += Offset
            self.cycles -= 1
            PageChange = (self.PC >> 8) != (OldPC >> 8)
            if PageChange:
                self.cycles -= 2

    def ADCALU(self, Operand: bytes, subtractMode=False) -> None:
        '''Handles bulk logic of ADC'''
        if self.D == 1: raise Exception("Decimal mode not implemented")
        oldA = self.A
        oldANFlag = self.A & 0b10000000
        OperandNFlag = Operand & 0b10000000
        Sum = self.A + Operand + self.C
        self.A = Sum & 0xFF
        self.SetZNFlags(self.A)
        if subtractMode == False:
            self.C = 1 if ((Sum & 0xFF00) > 0) and ((self.A & 0b10000000) <= 0) else 0
        if subtractMode == True:
            self.C = 1 if ((Sum & 0xFF00) > 0) and ((self.A & 0b10000000) <= 0) else self.C
        self.N = 1 if (self.A & 0b10000000) > 0 else self.N
        self.A = self.NegByte(self.A) if (self.N == 1) and (Sum < 0) else self.A
        self.V = 1 if (((OperandNFlag) ^ (oldANFlag)) == 0) and ((self.A & 0b10000000) != (OperandNFlag)) else 0
        self.C = 1 if (((OperandNFlag) and (oldANFlag)) > 0) else self.C
        self.C = 1 if ((OperandNFlag) != (oldANFlag)) and (self.A > 0) else self.C
        if subtractMode == True:
            if (((self.A-~Operand) & 0xFF00) > 0) or (self.V == 1):
                self.C = 0
            elif (self.V == 0) and ((oldA < 0) and (~Operand < 0)):
                self.C = 1 - self.C
            if ((oldA > 0) and (~Operand > 0)):
                self.C = 1 - self.C
        self.UpdatePS()

    def SBCALU(self, Operand: bytes) -> None:
        '''Handles bulk of logic for SBC'''
        self.ADCALU(~Operand, True)

    def CompareLogic(self, Operand: bytes, Register: bytes) -> None:
        '''Logic for all CMP address modes'''
        self.SetZNFlags(Register - Operand)
        self.C = 1 if Register >= Operand else 0

    def ASLLogic(self, Value: bytes) -> bytes:
        '''Handles ASL logic'''
        self.C = 1 if (Value & 0b10000000) > 0 else 0
        Value = (Value << 1) & 0xFF
        self.SetZNFlags(Value)
        self.cycles -= 1

        return Value

    def LSRLogic(self, Value: bytes) -> bytes:
        '''Handles LSR logic'''
        self.C = 1 if (Value & 0b1) > 0 else 0
        Value = (Value >> 1) & 0xFF
        self.SetZNFlags(Value)
        self.cycles -= 1

        return Value

    def ROLLogic(self, Value: bytes) -> bytes:
        '''Handles ROL logic'''
        Bit1 = self.C
        self.C = 1 if (Value & 0b10000000) > 0 else 0
        Value = (Value << 1) & 0xFF
        Value = Value | Bit1
        self.SetZNFlags(Value)
        if self.N == 1:
            Value = self.NegByte(Value)
        self.cycles -= 1

        return Value

    def RORLogic(self, Value: bytes) -> bytes:
        '''Handles ROR logic'''
        Bit7 = self.C
        self.C = 1 if (Value & 0b1) > 0 else 0
        Value = (Value >> 1) & 0xFF
        Value = Value | (Bit7 << 7)
        self.SetZNFlags(Value)
        if self.N == 1:
            Value = self.NegByte(Value)
        self.cycles -= 1

        return Value


    # Instruction Set

    # LDA
    INS_LDA_IM = 0xA9
    INS_LDA_ZP = 0xA5
    INS_LDA_ZPX = 0xB5
    INS_LDA_ABS = 0xAD
    INS_LDA_ABSX = 0xBD
    INS_LDA_ABSY = 0xB9
    INS_LDA_INDX = 0xA1
    INS_LDA_INDY = 0xB1
    # LDX
    INS_LDX_IM = 0xA2
    INS_LDX_ZP = 0xA6
    INS_LDX_ZPY = 0xB6
    INS_LDX_ABS = 0xAE
    INS_LDX_ABSY = 0xBE
    # LDY
    INS_LDY_IM = 0xA0
    INS_LDY_ZP = 0xA4
    INS_LDY_ZPX = 0xB4
    INS_LDY_ABS = 0xAC
    INS_LDY_ABSX = 0xBC
    # STA
    INS_STA_ZP = 0x85
    INS_STA_ZPX = 0x95
    INS_STA_ABS = 0x8D
    INS_STA_ABSX = 0x9D
    INS_STA_ABSY = 0x99
    INS_STA_INDX = 0x81
    INS_STA_INDY = 0x91
    # STX
    INS_STX_ZP = 0x86
    INS_STX_ZPY = 0x96
    INS_STX_ABS = 0x8E
    # STY
    INS_STY_ZP = 0x84
    INS_STY_ZPX = 0x94
    INS_STY_ABS = 0x8C
    # JSR, RTS, JMP
    INS_JSR = 0x20
    INS_JMP_ABS = 0x4C
    INS_JMP_IND = 0x6C
    INS_RTS = 0x60
    # TSX, TXS, PHA, PHP, PLA, PLP
    INS_TSX = 0xBA
    INS_TXS = 0x9A
    INS_PHA = 0x48
    INS_PHP = 0x08
    INS_PLA = 0x68
    INS_PLP = 0x28
    # AND
    INS_AND_IM = 0x29
    INS_AND_ZP = 0x25
    INS_AND_ZPX = 0x35
    INS_AND_ABS = 0x2D
    INS_AND_ABSX = 0x3D
    INS_AND_ABSY = 0x39
    INS_AND_INDX = 0x21
    INS_AND_INDY = 0x31
    # EOR
    INS_EOR_IM = 0x49
    INS_EOR_ZP = 0x45
    INS_EOR_ZPX = 0x55
    INS_EOR_ABS = 0x4D
    INS_EOR_ABSX = 0x5D
    INS_EOR_ABSY = 0x59
    INS_EOR_INDX = 0x41
    INS_EOR_INDY = 0x51
    # ORA
    INS_ORA_IM = 0x09
    INS_ORA_ZP = 0x05
    INS_ORA_ZPX = 0x15
    INS_ORA_ABS = 0x0D
    INS_ORA_ABSX = 0x1D
    INS_ORA_ABSY = 0x19
    INS_ORA_INDX = 0x01
    INS_ORA_INDY = 0x11
    # BIT
    INS_BIT_ZP = 0x24
    INS_BIT_ABS = 0x2C
    # TAX, TYX, TAX, TAY
    INS_TAX = 0xAA
    INS_TAY = 0xA8
    INS_TXA = 0x8A
    INS_TYA = 0x98
    # INX, INY, DEC, DEY
    INS_INX = 0xE8
    INS_INY = 0xC8
    INS_DEX = 0xCA
    INS_DEY = 0x88
    # DEC
    INS_DEC_ZP = 0xC6
    INS_DEC_ZPX = 0xD6
    INS_DEC_ABS = 0xCE
    INS_DEC_ABSX = 0xDE
    # INC
    INS_INC_ZP = 0xE6
    INS_INC_ZPX = 0xF6
    INS_INC_ABS = 0xEE
    INS_INC_ABSX = 0xFE
    # BCC, BCS, BEQ, BMI, BNE, BPL, BVS, BVC
    INS_BEQ = 0xF0
    INS_BNE = 0xD0
    INS_BCS = 0xB0
    INS_BCC = 0x90
    INS_BMI = 0x30
    INS_BPL = 0x10
    INS_BVS = 0x70
    INS_BVC = 0x50
    # CLC, CLD, CLI, CLV, SEC, SED, SEI 
    INS_CLC = 0x18
    INS_SEC = 0x38
    INS_CLD = 0xD8
    INS_CLI = 0x58
    INS_CLV = 0xB8
    INS_SED = 0xF8
    INS_SEI = 0x78
    # ADC
    INS_ADC_ABS = 0x6D
    INS_ADC_IM = 0x69
    INS_ADC_ZP = 0x65
    INS_ADC_ZPX = 0x75
    INS_ADC_ABSX = 0x7D
    INS_ADC_ABSY = 0x79
    INS_ADC_INDX = 0x61
    INS_ADC_INDY = 0x71
    # SBC
    INS_SBC_IM = 0xE9
    INS_SBC_ZP = 0xE5
    INS_SBC_ZPX = 0xF5
    INS_SBC_ABS = 0xED
    INS_SBC_ABSX = 0xFD
    INS_SBC_ABSY = 0xF9
    INS_SBC_INDX = 0xE1
    INS_SBC_INDY = 0xF1
    # NOP
    INS_NOP = 0xEA
    # CMP
    INS_CMP_IM = 0xC9
    INS_CMP_ZP = 0xC5
    INS_CMP_ZPX = 0xD5
    INS_CMP_ABS = 0xCD
    INS_CMP_ABSX = 0xDD
    INS_CMP_ABSY = 0xD9
    INS_CMP_INDX = 0xC1
    INS_CMP_INDY = 0xD1
    # CPX, CPY
    INS_CPX_IM = 0xE0
    INS_CPX_ZP = 0xE4
    INS_CPX_ABS = 0xEC
    INS_CPY_IM = 0xC0
    INS_CPY_ZP = 0xC4
    INS_CPY_ABS = 0xCC
    # ASL, LSR
    INS_ASL_AC = 0x0A
    INS_ASL_ZP = 0x06
    INS_ASL_ZPX = 0x16
    INS_ASL_ABS = 0x0E
    INS_ASL_ABSX = 0x1E
    INS_LSR_AC = 0x4A
    INS_LSR_ZP = 0x46
    INS_LSR_ZPX = 0x56
    INS_LSR_ABS = 0x4E
    INS_LSR_ABSX = 0x5E
    # ROL, ROR
    INS_ROL_AC = 0x2A
    INS_ROL_ZP = 0x26
    INS_ROL_ZPX = 0x36
    INS_ROL_ABS = 0x2E
    INS_ROL_ABSX = 0x3E
    INS_ROR_AC = 0x6A
    INS_ROR_ZP = 0x66
    INS_ROR_ZPX = 0x76
    INS_ROR_ABS = 0x6E
    INS_ROR_ABSX = 0x7E
    # BRK, RTI
    INS_BRK = 0x00
    INS_RTI = 0x40


    def Execute(self, cycles: int, memory: Mem) -> int:
        '''Handles all instructions; Starts CPU'''
        Requests = cycles
        self.cycles = cycles

        while self.cycles > 0:
            Ins = self.FetchByte(memory)

            if Ins == self.INS_LDA_IM:
                self.A = self.FetchByte(memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDX_IM:
                self.X = self.FetchByte(memory)
                self.SetZNFlags(self.X)

            elif Ins == self.INS_LDY_IM:
                self.Y = self.FetchByte(memory)
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_LDA_ZP:
                ZeroPageAddress = self.AddrZeroPage(memory)
                self.A = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDX_ZP:
                ZeroPageAddress = self.AddrZeroPage(memory)
                self.X = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.X)

            elif Ins == self.INS_LDY_ZP:
                ZeroPageAddress = self.AddrZeroPage(memory)
                self.Y = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_LDY_ZPX:
                ZeroPageAddress = self.AddrZeroPageXY(memory, self.X)
                self.Y = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_LDX_ZPY:
                ZeroPageAddress = self.AddrZeroPageXY(memory, self.Y)
                self.X = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.X)

            elif Ins == self.INS_LDA_ZPX:
                ZeroPageAddress = self.AddrZeroPageXY(memory, self.X)
                self.A = self.ReadByte(ZeroPageAddress, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDA_ABS:
                AbsoluteAddress = self.AddrAbsolute(memory)
                self.A = self.ReadByte(AbsoluteAddress, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDX_ABS:
                AbsoluteAddress = self.AddrAbsolute(memory)
                self.X = self.ReadByte(AbsoluteAddress, memory)
                self.SetZNFlags(self.X)

            elif Ins == self.INS_LDY_ABS:
                AbsoluteAddress = self.AddrAbsolute(memory)
                self.Y = self.ReadByte(AbsoluteAddress, memory)
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_LDA_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.A = self.ReadByte(Address, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDY_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.Y = self.ReadByte(Address, memory)
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_LDA_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                self.A = self.ReadByte(Address, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDX_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                self.X = self.ReadByte(Address, memory)
                self.SetZNFlags(self.X)

            elif Ins == self.INS_LDA_INDX:
                EffectiveAddress = self.AddrInderectX(memory)
                self.A = self.ReadByte(EffectiveAddress, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_LDA_INDY:
                EffectiveAddressY = self.AddrInderectY(memory)
                self.A = self.ReadByte(EffectiveAddressY, memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_STA_ZP:
                Address = self.AddrZeroPage(memory)
                memory = self.WriteByte(self.A, Address, memory)

            elif Ins == self.INS_STX_ZP:
                Address = self.AddrZeroPage(memory)
                memory = self.WriteByte(self.X, Address, memory)

            elif Ins == self.INS_STY_ZP:
                Address = self.AddrZeroPage(memory)
                memory = self.WriteByte(self.Y, Address, memory)

            elif Ins == self.INS_STA_ABS:
                Address = self.AddrAbsolute(memory)
                memory = self.WriteByte(self.A, Address, memory)

            elif Ins == self.INS_STX_ABS:
                Address = self.AddrAbsolute(memory)
                memory = self.WriteByte(self.X, Address, memory)

            elif Ins == self.INS_STY_ABS:
                Address = self.AddrAbsolute(memory)
                memory = self.WriteByte(self.Y, Address, memory)

            elif Ins == self.INS_STA_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                memory = self.WriteByte(self.A, Address, memory)

            elif Ins == self.INS_STX_ZPY:
                Address = self.AddrZeroPageXY(memory, self.Y)
                memory = self.WriteByte(self.X, Address, memory)

            elif Ins == self.INS_STY_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                memory = self.WriteByte(self.Y, Address, memory)

            elif Ins == self.INS_STA_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X, sta=True)
                memory = self.WriteByte(self.A, Address, memory)

            elif Ins == self.INS_STA_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y, sta=True)
                memory = self.WriteByte(self.A, Address, memory)

            elif Ins == self.INS_STA_INDX:
                EffectiveAddress = self.AddrInderectX(memory)
                memory = self.WriteByte(self.A, EffectiveAddress, memory)

            elif Ins == self.INS_STA_INDY:
                EffectiveAddressY = self.AddrInderectY(memory, sta=True)
                memory = self.WriteByte(self.A, EffectiveAddressY, memory)

            elif Ins == self.INS_JSR:
                SubAddr = self.FetchWord(memory)
                memory = self.PushPCToStack(memory)
                self.PC = SubAddr
                self.CheckPC()
                self.cycles -= 1

            elif Ins == self.INS_RTS:
                ReturnAddress = self.PopWordFromStack(memory)
                self.PC = ReturnAddress + 1
                self.cycles -= 2

            elif Ins == self.INS_JMP_ABS:
                Address = self.AddrAbsolute(memory)
                self.PC = Address

            elif Ins == self.INS_JMP_IND:
                Address = self.AddrAbsolute(memory)
                Address = self.ReadWord(Address, memory)
                self.PC = Address

            elif Ins == self.INS_TSX:
                self.X = self.SP
                self.cycles -= 1

            elif Ins == self.INS_TXS:
                self.SP = self.X
                self.cycles -= 1

            elif Ins == self.INS_PHA:
                memory = self.PushByteToStack(self.A, memory)

            elif Ins == self.INS_PHP:
                memory = self.PushByteToStack(self.PS, memory)

            elif Ins == self.INS_PLA:
                self.A = self.PopByteFromStack(memory)
                self.SetZNFlags(self.A)
                self.cycles -= 1

            elif Ins == self.INS_PLP:
                self.PS = self.PopByteFromStack(memory)
                self.PSToPSL()
                self.cycles -= 1

            elif Ins == self.INS_AND_IM:
                self.A = self.A & self.FetchByte(memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_EOR_IM:
                self.A = self.A ^ self.FetchByte(memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_ORA_IM:
                self.A = self.A | self.FetchByte(memory)
                self.SetZNFlags(self.A)

            elif Ins == self.INS_AND_ZP:
                Address = self.AddrZeroPage(memory)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_ZP:
                Address = self.AddrZeroPage(memory)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_ZP:
                Address = self.AddrZeroPage(memory)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_ABS:
                Address = self.AddrAbsolute(memory)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_ABS:
                Address = self.AddrAbsolute(memory)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_ABS:
                Address = self.AddrAbsolute(memory)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_INDX:
                Address = self.AddrInderectX(memory)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_INDX:
                Address = self.AddrInderectX(memory)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_INDX:
                Address = self.AddrInderectX(memory)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_AND_INDY:
                Address = self.AddrInderectY(memory)
                self.ANDRegister(Address, memory)

            elif Ins == self.INS_EOR_INDY:
                Address = self.AddrInderectY(memory)
                self.EORRegister(Address, memory)

            elif Ins == self.INS_ORA_INDY:
                Address = self.AddrInderectY(memory)
                self.ORARegister(Address, memory)

            elif Ins == self.INS_BIT_ZP:
                Address = self.AddrZeroPage(memory)
                self.BITTest(Address, memory)

            elif Ins == self.INS_BIT_ABS:
                Address = self.AddrAbsolute(memory)
                self.BITTest(Address, memory)

            elif Ins == self.INS_TAX:
                self.X = self.A
                self.SetZNFlags(self.X)
                self.cycles -= 1

            elif Ins == self.INS_TAY:
                self.Y = self.A
                self.SetZNFlags(self.Y)
                self.cycles -= 1

            elif Ins == self.INS_TXA:
                self.A = self.X
                self.SetZNFlags(self.A)
                self.cycles -= 1

            elif Ins == self.INS_TYA:
                self.A = self.Y
                self.SetZNFlags(self.A)
                self.cycles -= 1

            elif Ins == self.INS_INX:
                self.X += 1
                self.X = self.WrapByte(self.X)
                self.cycles -= 1
                self.SetZNFlags(self.X)

            elif Ins == self.INS_INY:
                self.Y += 1
                self.Y = self.WrapByte(self.Y)
                self.cycles -= 1
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_DEX:
                self.X -= 1
                self.X = self.WrapByte(self.X)
                self.cycles -= 1
                self.SetZNFlags(self.X)

            elif Ins == self.INS_DEY:
                self.Y -= 1
                self.Y = self.WrapByte(self.Y)
                self.cycles -= 1
                self.SetZNFlags(self.Y)

            elif Ins == self.INS_DEC_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value -= 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_DEC_ZPX:
                Address = self.AddrZeroPage(memory)
                Address += self.X
                Address = self.WrapByte(Address)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value -= 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_DEC_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value -= 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_DEC_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                Address = self.WrapWord(Address)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value -= 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_INC_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value += 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_INC_ZPX:
                Address = self.AddrZeroPage(memory)
                Address += self.X
                Address = self.WrapByte(Address)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value += 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_INC_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value += 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_INC_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                Address = self.WrapWord(Address)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value += 1
                Value = self.WrapByte(Value)
                self.cycles -= 1
                memory = self.WriteByte(Value, Address, memory)
                self.SetZNFlags(Value)

            elif Ins == self.INS_BEQ:
                self.BranchIf(1, self.Z, memory)

            elif Ins == self.INS_BNE:
                self.BranchIf(0, self.Z, memory)

            elif Ins == self.INS_BCS:
                self.BranchIf(1, self.C, memory)

            elif Ins == self.INS_BCC:
                self.BranchIf(0, self.C, memory)

            elif Ins == self.INS_BMI:
                self.BranchIf(1, self.N, memory)

            elif Ins == self.INS_BPL:
                self.BranchIf(0, self.N, memory)

            elif Ins == self.INS_BVS:
                self.BranchIf(1, self.V, memory)

            elif Ins == self.INS_BVC:
                self.BranchIf(0, self.V, memory)

            elif Ins == self.INS_CLC:
                self.C = 0
                self.cycles -= 1

            elif Ins == self.INS_SEC:
                self.C = 1
                self.cycles -= 1

            elif Ins == self.INS_CLD:
                self.D = 0
                self.cycles -= 1

            elif Ins == self.INS_CLI:
                self.I = 0
                self.cycles -= 1

            elif Ins == self.INS_CLV:
                self.V = 0
                self.cycles -= 1

            elif Ins == self.INS_SED:
                self.D = 1
                self.cycles -= 1

            elif Ins == self.INS_SEI:
                self.I = 1
                self.cycles -= 1

            elif Ins == self.INS_ADC_ABS:
                Address = self.AddrAbsolute(memory)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_IM:
                Operand = self.FetchByte(memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_ZP:
                Address = self.AddrZeroPage(memory)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_INDX:
                Address = self.AddrInderectX(memory)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_ADC_INDY:
                Address = self.AddrInderectY(memory)
                Operand = self.ReadByte(Address, memory)
                self.ADCALU(Operand)

            elif Ins == self.INS_CMP_IM:
                Operand = self.FetchByte(memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_ZP:
                Address = self.AddrZeroPage(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_ABS:
                Address = self.AddrAbsolute(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_INDX:
                Address = self.AddrInderectX(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CMP_INDY:
                Address = self.AddrInderectY(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.A)

            elif Ins == self.INS_CPX_IM:
                Operand = self.FetchByte(memory)
                self.CompareLogic(Operand, self.X)

            elif Ins == self.INS_CPX_ZP:
                Address = self.AddrZeroPage(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.X)

            elif Ins == self.INS_CPX_ABS:
                Address = self.AddrAbsolute(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.X)

            elif Ins == self.INS_CPY_IM:
                Operand = self.FetchByte(memory)
                self.CompareLogic(Operand, self.Y)

            elif Ins == self.INS_CPY_ZP:
                Address = self.AddrZeroPage(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.Y)

            elif Ins == self.INS_CPY_ABS:
                Address = self.AddrAbsolute(memory)
                Operand = self.ReadByte(Address, memory)
                self.CompareLogic(Operand, self.Y)

            elif Ins == self.INS_SBC_ABS:
                Address = self.AddrAbsolute(memory)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_IM:
                Operand = self.FetchByte(memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_ZP:
                Address = self.AddrZeroPage(memory)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_ABSY:
                Address = self.AddrAbsoluteXY(memory, self.Y)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_INDX:
                Address = self.AddrInderectX(memory)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_SBC_INDY:
                Address = self.AddrInderectY(memory)
                Operand = self.ReadByte(Address, memory)
                self.SBCALU(Operand)

            elif Ins == self.INS_ASL_AC:
                self.A = self.ASLLogic(self.A)

            elif Ins == self.INS_ASL_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.ASLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ASL_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Value = self.ReadByte(Address, memory)
                Value = self.ASLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ASL_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.ASLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ASL_ABSX:
                oldC = self.cycles
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value = self.ASLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_LSR_AC:
                self.A = self.LSRLogic(self.A)

            elif Ins == self.INS_LSR_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.LSRLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_LSR_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Value = self.ReadByte(Address, memory)
                Value = self.LSRLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_LSR_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.LSRLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_LSR_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value = self.LSRLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROL_AC:
                self.A = self.ROLLogic(self.A)

            elif Ins == self.INS_ROL_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.ROLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROL_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Value = self.ReadByte(Address, memory)
                Value = self.ROLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROL_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.ROLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROL_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value = self.ROLLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROR_AC:
                self.A = self.RORLogic(self.A)

            elif Ins == self.INS_ROR_ZP:
                Address = self.AddrZeroPage(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.RORLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROR_ZPX:
                Address = self.AddrZeroPageXY(memory, self.X)
                Value = self.ReadByte(Address, memory)
                Value = self.RORLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROR_ABS:
                Address = self.AddrAbsolute(memory)
                Value = self.ReadByte(Address, memory)
                Value = self.RORLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_ROR_ABSX:
                Address = self.AddrAbsoluteXY(memory, self.X)
                self.cycles -= 1
                Value = self.ReadByte(Address, memory)
                Value = self.RORLogic(Value)
                memory = self.WriteByte(Value, Address, memory)

            elif Ins == self.INS_BRK:
                memory = self.PushPCToStack(memory)
                memory = self.PushByteToStack(self.PS, memory)
                self.PC = self.ReadWord(0xFFFE, memory)
                self.B = 1

            elif Ins == self.INS_RTI:
                self.PS = self.PopByteFromStack(memory)
                self.PC = self.PopWordFromStack(memory)
                self.PC += 1

            elif Ins == self.INS_NOP:
                self.cycles -= 1

            else:
                pastPC = self.PC - 1
                if pastPC < 0:
                    pastPC = 0xFFFF
                raise Exception("Unknown Instruction at address %s: %s" % (hex(pastPC), hex(Ins)))

        return Requests - self.cycles
