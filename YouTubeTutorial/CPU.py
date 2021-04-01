from typing import Any

from InsCodes import *
from Memory import Memory


class CPUException(Exception):
    pass


class Flags:
    def __init__(self):
        self.Z = 0 # Zero
        self.C = 0 # Carry
        self.O = 0 # Overflow
        self.S = 0 # Sign
        self.B = 0 # Busy
        self.T = 0 # Trap
        self.I = 0 # Interupt Disable
        self.E = 0 # Interupt

    def full(self):
        ps = self.Z << 7 | self.C << 6 | self.O << 5 | self.S << 4 | self.B << 3 | self.T << 2 | self.I << 1 | self.E
        return ps


class CPU:

    Syscall = 0x80
    COM0 = 0xFFB
    IntLoc = 0xFFA

    reserved            = 0x00
    SingleStepInterrupt = 0x01
    Breakpoint          = 0x03
    InvalidOpcode       = 0x06
    DoubleFault         = 0x08
    OutOfMemory         = 0x16

    Sys_RestartSyscall = 0x00

    Sys_Exit = 0x01
    Sys_Fork = 0x02
    Sys_Read = 0x03
    Sys_Write = 0x04
    Sys_Open = 0x05
    Sys_Close = 0x06
    Sys_Creat = 0x08
    Sys_Time = 0x0D
    Sys_fTime = 0x23

    def __init__(self):
        '''CPU object that interpretes and runs binary as machine code.

        ```
        from CPU import CPU

        cpu = CPU()
        cpu.Start()
        ```
        '''
        self.PC = 0x00000000 # Program Counter
        self.PS = Flags() # Processor Status

        self.Memory = Memory().Data
        self.Buffer = len(self.Memory) # 64 kb

        # 32-bit General
        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.EDI = 0
        self.ESI = 0
        self.ESP = 0 # Stack Pointer
        self.EBP = 0 # Base Pointer

        # 16-bit General
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0

        # 8-bit General
        self.BAX = 0
        self.BBX = 0
        self.BCX = 0
        self.BDX = 0

        self.Debug = False
        self.Cycles = 0
        self.InInterupt = False

    def LoadMemory(self, memory: Memory) -> None:
        '''Loads Memory object contents into local RAM
        
        ```
        cpu = CPU()
        mem = Memory()

        mem.Data[0] = 42
        cpu.LoadMemory(mem)
        ```
        '''
        self.Memory = memory.Data
        self.Buffer = len(self.Memory)

    def __FetchByte(self) -> int:
        byte = self.Memory[self.PC]
        self.PC += 1
        self.Cycles -= 1

        return byte

    def __FetchWord(self) -> int:
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __WriteReg(self, code: int, value: int) -> None:
        if code == Code_EAX:
            self.EAX = value

        elif code == Code_EBX:
            self.EBX = value

        elif code == Code_ECX:
            self.ECX = value

        elif code == Code_EDX:
            self.EDX = value

        self.Cycles -= 1

    def __GetReg(self, code: int) -> None:
        self.Cycles -= 1

        if code == Code_EAX:
            return self.EAX

        elif code == Code_EBX:
            return self.EBX

        elif code == Code_ECX:
            return self.ECX

        elif code == Code_EDX:
            return self.EDX

    def __RaiseInterrupt(self, code: int, **kwargs) -> None:
        try:
            string = "CPU: Interrupt: "

            if code == self.InvalidOpcode:
                if 'opcode' in kwargs:
                    string += "InvalidOpcode: %s at addr %s" % (hex(kwargs['opcode']), hex(self.PC-1))

                else:
                    string += "InvalidOpcode: Unknown at addr %s" % hex(self.PC-1)

            elif code == self.OutOfMemory:
                string += "OutOfMemory: %s" % hex(self.PC)

            elif code == self.SingleStepInterrupt:
                string += "SingleStepInterrupt: %s" % hex(self.PC)
                input(string)
                return

            elif code == self.Breakpoint:
                string += "Breakpoint: %s" % hex(self.PC-1)
                input(string)
                return

        except Exception as e:
            if self.Debug:
                print("CPU: Interrupt: DoubleFault: Origin: %s" % e)
            
            raise CPUException(string + "DoubleFault: %s" % hex(self.PC))

        raise CPUException(string)

    def __HandleSyscall(self):
        if self.EAX == self.Sys_Write:
            if self.EBX == 1:
                string = ''
                counter = 0

                while counter < self.EDX:
                    char = self.Memory[self.ECX + counter]
                    self.Cycles -= 1
                    string += chr(char)
                    counter += 1

                if self.Debug:
                    print("CPU: Interrupt: Syscall: Write: Stdout: %s" % string)

                else:
                    print(string, end='')

        elif self.EAX == self.Sys_Exit:
            raise CPUException("CPU Exited with code %d (%s)" % (self.EBX, hex(self.EBX)))

    def __HandleInterrupt(self) -> None:
        if self.Memory[self.IntLoc] == self.Syscall:
            self.__HandleSyscall()

        else:
            self.__RaiseInterrupt(self.Memory[self.IntLoc])

        self.InInterupt = True
        self.PS.E = 0

    def Start(self):
        try:
            self.Execute('inf')

        except CPUException as e:
            print(e)

    def Execute(self, cycles: int) -> Any:
        if cycles != 'inf':
            self.Cycles = cycles

        while (self.Cycles > 0) or (cycles == 'inf'):
            if self.PS.T:
                self.__RaiseInterrupt(self.SingleStepInterrupt)

            ins = self.__FetchByte()

            if ins == NOP:
                pass

            elif ins == 0xCC:
                self.__RaiseInterrupt(self.Breakpoint)

            elif ins == MOV:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, value)

                elif mod == Addr_RegIm16:
                    reg = self.__FetchByte()
                    value = self.__FetchWord()
                    self.__WriteReg(reg, value)

            elif ins == INT:
                intCode = self.__FetchByte()
                self.Memory[self.IntLoc] = intCode
                self.__HandleInterrupt()

            elif ins == ADD:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, value + self.__GetReg(reg))

            elif ins == SUB:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, self.__GetReg(reg) - value)

            elif ins == DIV:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, round(self.__GetReg(reg) / value))

            elif ins == MUL:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    self.__WriteReg(reg, round(value * self.__GetReg(reg)))

            elif ins == INC:
                mod = self.__FetchByte()

                if mod == Addr_Reg:
                    reg = self.__FetchByte()
                    self.__WriteReg(reg, self.__GetReg(reg) + 1)

            elif ins == DEC:
                mod = self.__FetchByte()

                if mod == Addr_Reg:
                    reg = self.__FetchByte()
                    self.__WriteReg(reg, self.__GetReg(reg) - 1)

            elif ins == CMP:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    value = self.__FetchByte()
                    reg = self.__GetReg(reg)
                    result = reg - value

                    if result == 0:
                        self.PS.Z = 1

                    elif result > 0:
                        self.PS.S = 0

                    elif result < 0:
                        self.PS.S = 1

            elif ins == JMP:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()
                    self.PC = value
                    self.Cycles -= 1

            elif ins == JE:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if self.PS.Z == 1:
                        self.PC = value
                        self.Cycles -= 1

            elif ins == JNE:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if self.PS.Z == 0:
                        self.PC = value
                        self.Cycles -= 1

            elif ins == JG:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if self.PS.S == 0:
                        self.PC = value
                        self.Cycles -= 1

            elif ins == JGE:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if (self.PS.S == 0) or (self.PS.Z == 1):
                        self.PC = value
                        self.Cycles -= 1

            elif ins == JL:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if self.PS.S:
                        self.PC = value
                        self.Cycles -= 1

            elif ins == JLE:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()

                    if (self.PS.Z) or (self.PS.S):
                        self.PC = value
                        self.Cycles -= 1

            elif ins == HLT:
                return

            else:
                self.__RaiseInterrupt(self.InvalidOpcode, opcode=ins)

        ret = None

        if self.Debug:
            if cycles == 'inf':
                ret = cycles

            else:
                ret = cycles - self.Cycles

        return ret
