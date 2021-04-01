import re
import msvcrt

from Source import *
from Codes import *

class CPUException(Exception):
    pass

class CPU:

    Type = 0x454D50
    Family = 0x0064
    Model = 0x1000
    __ID = 0x00

    Sys_Read     = 0x00
    Sys_Write    = 0x01
    Sys_Open     = 0x02
    Sys_Close    = 0x03
    Sys_Exit     = 0x3C
    Sys_Chdir    = 0x50
    Sys_Rename   = 0x52
    Sys_Mkdir    = 0x53
    Sys_Rmdir    = 0x54
    Sys_Creat    = 0x55
    Sys_Sysinfo  = 0x63
    Sys_Time     = 0xC9

    Syscalls = {
        0x00: 'read', 0x01: 'write', 0x02: 'open', 0x03: 'close',
        0x3C: 'exit', 0x50: 'chdir', 0x52: 'rename', 0x53: 'mkdir',
        0x54: 'rmdir', 0x55: 'creat', 0x63: 'sysinfo', 0xC9: 'time'
    }

    SingleStepInterrupt = 0x01
    Breakpoint          = 0x02
    InvalidOpcode       = 0x03
    AddressNotPresent   = 0x04

    def __init__(self):
        '''# EMP64 CPU.

        This CPU will execution instructions written about in the EMP64 Manual.
        To use you must call LoadMemory(n) with a Memory object supplied with the EMP64 source files.
        Then you just call Start() and the CPU will start execution at address 0x0 of the loaded memory.

        ## Example

        ```
        from Codes import *
        from Source import Memory
        from CPU import CPU

        mem = Memory(0xFFFFFF)
        cpu = CPU()

        mem.Data[0x0] = Pre_8 | Addr_RegIm
        mem.Data[0x1] = MOV
        mem.Data[0x2] = Reg_RAX
        mem.Data[0x3] = CPU.Sys_Exit
        mem.Data[0x4] = SYSCALL

        cpu.LoadMemory(mem)
        cpu.Start()
        ```

        ```txt
        >>> EMP64-1000 0: Exited with code 0 (0x0).
        ```
        '''

        # 64-bit General Purpose Registers
        self.RAX = 0
        self.RBX = 0
        self.RCX = 0
        self.RDX = 0
        self.RSI = 0
        self.RDI = 0
        self.RBP = 0
        self.RSP = 0xFFFF
        self.R8 = 0
        self.R9 = 0
        self.R10 = 0
        self.R11 = 0
        self.R12 = 0
        self.R13 = 0
        self.R14 = 0
        self.R15 = 0

        # 128-bit Floating Point Registers
        self.SSE0 = 0
        self.SSE1 = 0
        self.SSE2 = 0
        self.SSE3 = 0
        self.SSE4 = 0
        self.SSE5 = 0
        self.SSE6 = 0
        self.SSE7 = 0
        self.SSE8 = 0
        self.SSE9 = 0
        self.SSE10 = 0
        self.SSE11 = 0
        self.SSE12 = 0
        self.SSE13 = 0
        self.SSE14 = 0
        self.SSE15 = 0

        # 80-bit Floating Point Registers
        self.EES0 = 0
        self.EES0 = 1
        self.EES0 = 2
        self.EES0 = 3
        self.EES0 = 4
        self.EES0 = 5
        self.EES0 = 6
        self.EES0 = 7

        # 64-bit Floating Point Registers
        self.MMX0 = 0
        self.MMX0 = 1
        self.MMX0 = 2
        self.MMX0 = 3
        self.MMX0 = 4
        self.MMX0 = 5
        self.MMX0 = 6
        self.MMX0 = 7

        # 512-bit Extended Registers
        self.ZMM0 = 0
        self.ZMM1 = 0
        self.ZMM2 = 0
        self.ZMM3 = 0
        self.ZMM4 = 0
        self.ZMM5 = 0
        self.ZMM6 = 0
        self.ZMM7 = 0
        self.ZMM8 = 0
        self.ZMM9 = 0
        self.ZMM10 = 0
        self.ZMM11 = 0
        self.ZMM12 = 0
        self.ZMM13 = 0
        self.ZMM14 = 0
        self.ZMM15 = 0

        # Special Registers
        self.RIP = 0
        self.EFLAGS = EFLAGS()
        self.IA32_EFER = IA32_EFER()
        self.DR0 = 0
        self.DR1 = 0
        self.DR2 = 0
        self.DR3 = 0
        self.DR6 = DR6()
        self.DR7 = DR7()
        self.TR6 = 0
        self.TR7 = 0
        self.GDTR = TR()
        self.LDTR = 0
        self.TR = 0
        self.IDTR = TR()
        self.TSS = TSS()

        # Class Variables
        self.Buffer = 0
        self.Mem = []
        self.Cycles = 0
        self.IRQ = False
        self.NMI = False

    def __PushByte(self, value: int):
        self.Mem[self.RSP] = value
        self.RSP -= 1
        self.Cycles += 1

    def __PopByte(self) -> int:
        self.RSP += 1
        value = self.Mem[self.RSP]
        self.Cycles += 1

        return value

    def __GetID(self) -> str:
        return '%s%s-%s %s' % ((chr((self.Type & 0xFF0000) >> 16) + chr((self.Type & 0xFF00) >> 8) + chr(self.Type & 0xFF)), hex(self.Family)[2:], hex(self.Model)[2:], self.__ID)

    def __WriteByte(self, address: int, value: int):
        if address >= self.Buffer:
            self.__RaiseInterrupt(self.AddressNotPresent)

        self.Mem[address] = value
        self.Cycles += 1

    def __WriteWord(self, address: int, value: int):
        self.__WriteByte(address, (value & 0xFF00) >> 8)
        self.__WriteByte(address+1, value & 0xFF)

    def __WriteDWord(self, address: int, value: int):
        self.__WriteWord(address, (value & 0xFFFF0000) >> 16)
        self.__WriteWord(address+2, value & 0xFFFF)

    def __WriteQWord(self, address: int, value: int):
        self.__WriteDWord(address, (value & 0xFFFFFFFF00000000) >> 32)
        self.__WriteDWord(address+4, value & 0xFFFFFFFF)

    def __ReadByte(self, address: int) -> int:
        if address >= self.Buffer:
            self.__RaiseInterrupt(self.AddressNotPresent, addr=address)

        value = self.Mem[address]
        self.Cycles += 1

        return value

    def __ReadWord(self, address: int) -> int:
        return self.__ReadByte(address) << 8 | self.__ReadByte(address + 1)

    def __ReadDWord(self, address: int) -> int:
        return self.__ReadWord(address) << 16 | self.__ReadWord(address + 2)

    def __ReadQWord(self, address: int) -> int:
        return self.__ReadDWord(address) << 32 | self.__ReadDWord(address + 4)

    def __FetchByte(self) -> int:
        if self.RIP >= self.Buffer:
            self.__RaiseInterrupt(self.AddressNotPresent)

        value = self.Mem[self.RIP]
        self.RIP += 1
        self.Cycles += 1

        return value

    def __FetchWord(self) -> int:
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __FetchDWord(self) -> int:
        return self.__FetchWord() << 16 | self.__FetchWord()

    def __FetchQWord(self) -> int:
        return self.__FetchDWord() << 32 | self.__FetchDWord()

    def __SetReg(self, code: int, value: int, size=0x64):
        anded = 0

        if size == 0x8:
            anded = 0xFFFFFFFFFFFFFF00

        elif size == 0x16:
            anded = 0xFFFFFFFFFFFF0000

        elif size == 0x32:
            anded = 0xFFFFFFFF00000000

        elif size == 0x128:
            anded = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000000000000000000000000000

        elif size == 0x256:
            anded = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000000000000000000000000000000000000000

        if size in [0x8, 0x16, 0x32, 0x64]:
            if code == 0:
                self.RAX = (self.RAX & anded) | value

            elif code == 1:
                self.RBX = (self.RBX & anded) | value

            elif code == 2:
                self.RCX = (self.RCX & anded) | value

            elif code == 3:
                self.RDX = (self.RDX & anded) | value

            elif code == 4:
                self.RSI = (self.RSI & anded) | value

            elif code == 5:
                self.RDI = (self.RDI & anded) | value

            elif code == 6:
                self.RBP = (self.RBP & anded) | value

            elif code == 7:
                self.RSP = (self.RSP & anded) | value

            elif code == 8:
                self.R8 = (self.R8 & anded) | value

            elif code == 9:
                self.R9 = (self.R9 & anded) | value

            elif code == 10:
                self.R10 = (self.R10 & anded) | value

            elif code == 11:
                self.R11 = (self.R11 & anded) | value

            elif code == 12:
                self.R12 = (self.R12 & anded) | value

            elif code == 13:
                self.R13 = (self.R13 & anded) | value

            elif code == 14:
                self.R14 = (self.R14 & anded) | value

            elif code == 15:
                self.R15 = (self.R15 & anded) | value

        elif size in [0x128, 0x256, 0x512]:
            if code == 0:
                self.ZMM0 = (self.ZMM0 & anded) | value

            elif code == 1:
                self.ZMM1 = (self.ZMM1 & anded) | value

            elif code == 2:
                self.ZMM2 = (self.ZMM2 & anded) | value

            elif code == 3:
                self.ZMM3 = (self.ZMM3 & anded) | value

            elif code == 4:
                self.ZMM4 = (self.ZMM4 & anded) | value

            elif code == 5:
                self.ZMM5 = (self.ZMM5 & anded) | value

            elif code == 6:
                self.ZMM6 = (self.ZMM6 & anded) | value

            elif code == 7:
                self.ZMM7 = (self.ZMM7 & anded) | value

            elif code == 8:
                self.ZMM8 = (self.ZMM8 & anded) | value

            elif code == 9:
                self.ZMM9 = (self.ZMM9 & anded) | value

            elif code == 10:
                self.ZMM10 = (self.ZMM10 & anded) | value

            elif code == 11:
                self.ZMM11 = (self.ZMM11 & anded) | value

            elif code == 12:
                self.ZMM12 = (self.ZMM12 & anded) | value

            elif code == 13:
                self.ZMM13 = (self.ZMM13 & anded) | value

            elif code == 14:
                self.ZMM14 = (self.ZMM14 & anded) | value

            elif code == 15:
                self.ZMM15 = (self.ZMM15 & anded) | value

        elif size == 0x64F:
            if code == 0:
                self.MMX0 = value

            elif code == 1:
                self.MMX1 = value

            elif code == 2:
                self.MMX2 = value

            elif code == 3:
                self.MMX3 = value

            elif code == 4:
                self.MMX4 = value

            elif code == 5:
                self.MMX5 = value

            elif code == 6:
                self.MMX6 = value

            elif code == 7:
                self.MMX7 = value

        elif size == 0x80F:
            if code == 0:
                self.EES0 = value

            elif code == 1:
                self.EES1 = value

            elif code == 2:
                self.EES2 = value

            elif code == 3:
                self.EES3 = value

            elif code == 4:
                self.EES4 = value

            elif code == 5:
                self.EES5 = value

            elif code == 6:
                self.EES6 = value

            elif code == 7:
                self.EES7 = value

        elif size == 0x128F:
            if code == 0:
                self.SSE0 = value

            elif code == 1:
                self.SSE1 = value

            elif code == 2:
                self.SSE2 = value

            elif code == 3:
                self.SSE3 = value

            elif code == 4:
                self.SSE4 = value

            elif code == 5:
                self.SSE5 = value

            elif code == 6:
                self.SSE6 = value

            elif code == 7:
                self.SSE7 = value

    def __GetReg(self, code: int, size=0x64):
        anded = 0

        if size == 0x8:
            anded = 0xFF

        elif size == 0x16:
            anded = 0xFFFF

        elif size == 0x32:
            anded = 0xFFFFFFFF

        elif size == 0x64:
            anded = 0xFFFFFFFFFFFFFFFF

        elif size == 0x128:
            anded = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        elif size == 0x256:
            anded = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        elif size == 0x512:
            anded = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        if size in [0x8, 0x16, 0x32, 0x64]:
            if code == 0:
                return self.RAX & anded

            elif code == 1:
                return self.RBX & anded

            elif code == 2:
                return self.RCX & anded

            elif code == 3:
                return self.RDX & anded

            elif code == 4:
                return self.RSI & anded

            elif code == 5:
                return self.RDI & anded

            elif code == 6:
                return self.RBP & anded

            elif code == 7:
                return self.RSP & anded

            elif code == 8:
                return self.R8 & anded

            elif code == 9:
                return self.R9 & anded

            elif code == 10:
                return self.R10 & anded

            elif code == 11:
                return self.R11 & anded

            elif code == 12:
                return self.R12 & anded

            elif code == 13:
                return self.R13 & anded

            elif code == 14:
                return self.R14 & anded

            elif code == 15:
                return self.R15 & anded

        elif size in [0x128, 0x256, 0x512]:
            if code == 0:
                return self.ZMM0 & anded

            elif code == 1:
                return self.ZMM1 & anded

            elif code == 2:
                return self.ZMM2 & anded

            elif code == 3:
                return self.ZMM3 & anded

            elif code == 4:
                return self.ZMM4 & anded

            elif code == 5:
                return self.ZMM5 & anded

            elif code == 6:
                return self.ZMM6 & anded

            elif code == 7:
                return self.ZMM7 & anded

            elif code == 8:
                return self.ZMM8 & anded

            elif code == 9:
                return self.ZMM9 & anded

            elif code == 10:
                return self.ZMM10 & anded

            elif code == 11:
                return self.ZMM11 & anded

            elif code == 12:
                return self.ZMM12 & anded

            elif code == 13:
                return self.ZMM13 & anded

            elif code == 14:
                return self.ZMM14 & anded

            elif code == 15:
                return self.ZMM15 & anded

        elif size == 0x64F:
            if code == 0:
                return self.MMX0

            elif code == 1:
                return self.MMX1

            elif code == 2:
                return self.MMX2

            elif code == 3:
                return self.MMX3

            elif code == 4:
                return self.MMX4

            elif code == 5:
                return self.MMX5

            elif code == 6:
                return self.MMX6

            elif code == 7:
                return self.MMX7

        elif size == 0x80F:
            if code == 0:
                return self.EES0

            elif code == 1:
                return self.EES1

            elif code == 2:
                return self.EES2

            elif code == 3:
                return self.EES3

            elif code == 4:
                return self.EES4

            elif code == 5:
                return self.EES5

            elif code == 6:
                return self.EES6

            elif code == 7:
                return self.EES7

        elif size == 0x128F:
            if code == 0:
                return self.SSE0

            elif code == 1:
                return self.SSE1

            elif code == 2:
                return self.SSE2

            elif code == 3:
                return self.SSE3

            elif code == 4:
                return self.SSE4

            elif code == 5:
                return self.SSE5

            elif code == 6:
                return self.SSE6

            elif code == 7:
                return self.SSE7

    def __GetClosestSyscall(self, code: int) -> list:
        value = min(self.Syscalls, key=lambda x:abs(x-code))

        return [value, self.Syscalls[value]]

    def __HandleSyscall(self):
        if self.RAX == self.Sys_Write:
            if self.RDI == 1:
                string = ''

                for i in range(self.RDX):
                    char = self.__ReadByte(self.RSI + i + self.RBP)
                    string += chr(char)

                print(string, end='')

        elif self.RAX == self.Sys_Read:
            if self.RDI == 1:
                string = ''

                for i in range(self.RDX):
                    char = msvcrt.getch().decode()

                    if char == '\r':
                        string += '\n'
                        break

                    string += char
                    print(string, end='\r')

                print(string, end='')

                for i in range(self.RDX):
                    try:
                        self.__WriteByte(self.RSI + i + self.RBP, ord(string[i]))

                    except IndexError:
                        break

        elif self.RAX == self.Sys_Exit:
            raise CPUException('\n%s: Exited with code %s (%s).' % (self.__GetID(), self.RDI, hex(self.RDI)))

        else:
            raise CPUException('\n%s: Exception: Undefined syscall code %s called at %s. Maybe you meant %s() (%s)'
                % (self.__GetID(), hex(self.RAX), hex(self.RIP - 1), self.__GetClosestSyscall(self.RAX)[1], hex(self.__GetClosestSyscall(self.RAX)[0])))

    def __RaiseInterrupt(self, code: int, **kwargs):
        try:
            string = '\n%s: ' % self.__GetID()

            if code == self.SingleStepInterrupt:
                string += 'SingleStepInterrupt: %s.' % hex(self.RIP)
                input(string)
                return

            elif code == self.Breakpoint:
                string += 'Breakpoint: %s.' % hex(self.RIP)
                input(string)
                return

            elif code == self.InvalidOpcode:
                string += 'InvalidOpcode: Invalid opcode %s found at address %s.' % (hex(kwargs['opcode']), hex(self.RIP-2))

            elif code == self.AddressNotPresent:
                if 'addr' in kwargs:
                    string += 'AddressNotPresent: Address %s is not present in RAM.\nThis was most likely caused by trying to access this memory directly.' % hex(kwargs['addr'])

                else:
                    string += 'AddressNotPresent: Address %s is not present in RAM.\nThis may be an OutOfMemory error. Try using exit() syscall to stop execution to avoid this error.' % hex(self.RIP)

        except Exception as e:
            raise CPUException(string + 'DoubleFault: %s' % e)

        raise CPUException(string)

    def __HandleInterrupt(self):
        if (self.IRQ == 0x80) or (self.NMI == 0x80):
            self.__HandleSyscall()

        else:
            if self.IRQ:
                self.__RaiseInterrupt(self.IRQ)

            if self.NMI:
                self.__RaiseInterrupt(self.NMI)

    def __CheckForInterrupt(self) -> bool:
        ret = False

        if self.NMI:
            self.__HandleInterrupt()
            self.NMI = False
            ret = True

        if self.EFLAGS.IF:
            if self.IRQ:
                self.__HandleInterrupt()
                self.IRQ = False
                ret = True

        return ret

    def LoadMemory(self, memory: Memory):
        '''#### Loads a Memory object into local memory.

        Updates CPU.Mem and CPU.Buffer'''

        self.Mem = memory.Data
        self.Buffer = len(self.Mem)

    def Start(self):
        '''#### Starts CPU execution starting at address 0x0.

        This will automatically wrap CPUExceptions only and print them. Other exceptions are not handled.

        A CPUException could be an interrupt, or some simple error detection e.g. invalid kernal call.'''

        try:
            self.__Execute()

        except CPUException as e:
            print(e)

    def LoadProgram(self, filename: str, loc: int):
        '''#### Loads a files contents into memory starting at a location.'''

        with open(filename + '.bin', 'rb') as f:
            contents = f.read().hex()
            contents = re.findall("..", contents)
            contents = [int(i, 16) for i in contents]

        self.Mem[0] = Pre_8 | Addr_RegIm
        self.Mem[1] = MOV
        self.Mem[2] = Reg_RBP
        self.Mem[3] = 14
        self.Mem[4] = Pre_64 | Addr_Im
        self.Mem[5] = CALL
        self.Mem[6] = (loc & 0xFF00000000000000) >> 56
        self.Mem[7] = (loc & 0xFF000000000000) >> 48
        self.Mem[8] = (loc & 0xFF0000000000) >> 40
        self.Mem[9] = (loc & 0xFF00000000) >> 32
        self.Mem[10] = (loc & 0xFF000000) >> 24
        self.Mem[11] = (loc & 0xFF0000) >> 16
        self.Mem[12] = (loc & 0xFF00) >> 8
        self.Mem[13] = loc & 0xFF

        for i in range(len(contents)):
            self.Mem[loc+i+14] = contents[i]

    def __Ins_MOV(self, pre: int):
        if pre & 0xF0 == Pre_8:
            if pre & 0xF == Addr_RegIm:
                reg = self.__FetchByte()
                value = self.__FetchByte()
                self.__SetReg(reg, value, size=0x8)

            elif pre & 0xF == Addr_RegDisp:
                reg = self.__FetchByte()
                address = self.__FetchQWord()
                value = self.__ReadByte(address + self.RBP)
                self.__SetReg(reg, value, size=0x8)

            elif pre & 0xF == Addr_RegReg:
                reg1 = self.__FetchByte()
                reg2 = self.__FetchByte()
                self.__SetReg(reg1, self.__GetReg(reg2, 0x8), 0x8)

            elif pre & 0xF == Addr_DispReg:
                address = self.__FetchQWord()
                reg = self.__FetchByte()
                self.__WriteByte(address + self.RBP, self.__GetReg(reg, 0x8))

        elif pre & 0xF0 == Pre_16:
            if pre & 0xF == Addr_RegIm:
                reg = self.__FetchByte()
                value = self.__FetchWord()
                self.__SetReg(reg, value, size=0x16)

            elif pre & 0xF == Addr_RegDisp:
                reg = self.__FetchByte()
                address = self.__FetchQWord()
                value = self.__ReadWord(address + self.RBP)
                self.__SetReg(reg, value, size=0x16)

            elif pre & 0xF == Addr_RegReg:
                reg1 = self.__FetchByte()
                reg2 = self.__FetchByte()
                self.__SetReg(reg1, self.__GetReg(reg2, 0x16), 0x16)

            elif pre & 0xF == Addr_DispReg:
                address = self.__FetchQWord()
                reg = self.__FetchByte()
                self.__WriteWord(address + self.RBP, self.__GetReg(reg, 0x16))

        elif pre & 0xF0 == Pre_32:
            if pre & 0xF == Addr_RegIm:
                reg = self.__FetchByte()
                value = self.__FetchDWord()
                self.__SetReg(reg, value, size=0x32)

            elif pre & 0xF == Addr_RegDisp:
                reg = self.__FetchByte()
                address = self.__FetchQWord()
                value = self.__ReadDWord(address + self.RBP)
                self.__SetReg(reg, value, size=0x32)

            elif pre & 0xF == Addr_RegReg:
                reg1 = self.__FetchByte()
                reg2 = self.__FetchByte()
                self.__SetReg(reg1, self.__GetReg(reg2, 0x32), 0x32)

            elif pre & 0xF == Addr_DispReg:
                address = self.__FetchQWord()
                reg = self.__FetchByte()
                self.__WriteDWord(address + self.RBP, self.__GetReg(reg, 0x32))

        elif pre & 0xF0 == Pre_64:
            if pre & 0xF == Addr_RegIm:
                reg = self.__FetchByte()
                value = self.__FetchQWord()
                self.__SetReg(reg, value, size=0x64)

            elif pre & 0xF == Addr_RegDisp:
                reg = self.__FetchByte()
                address = self.__FetchQWord()
                value = self.__ReadQWord(address + self.RBP)
                self.__SetReg(reg, value, size=0x64)

            elif pre & 0xF == Addr_RegReg:
                reg1 = self.__FetchByte()
                reg2 = self.__FetchByte()
                self.__SetReg(reg1, self.__GetReg(reg2, 0x64), 0x64)

            elif pre & 0xF == Addr_DispReg:
                address = self.__FetchQWord()
                reg = self.__FetchByte()
                self.__WriteQWord(address + self.RBP, self.__GetReg(reg, 0x64))

    def __Execute(self):
        while True:
            self.__CheckForInterrupt()

            if self.EFLAGS.TF:
                self.__RaiseInterrupt(self.SingleStepInterrupt)

            pre = self.__FetchByte()

            if pre == NOP:
                continue

            elif pre == HLT:
                while True:
                    if self.__CheckForInterrupt():
                        break

                continue

            elif pre == CPUID:
                if self.RBX == 1:
                    self.RDX = 0x722077696c736f6e

                else:
                    self.RDX = 0x494C6B4573746572

                self.RAX = self.Buffer
                self.RBX = self.Type << 40 | self.Family << 24 | self.Model << 8 | self.__ID
                self.RCX = self.Cycles

                continue

            elif pre == RET:
                self.RIP = self.__PopByte() + 1
                continue

            elif pre == SYSCALL:
                self.RCX = self.RIP
                self.R11 = self.EFLAGS.full()
                self.__HandleSyscall()
                self.RIP = self.RCX
                self.EFLAGS.load(self.R11)
                continue

            elif pre == 0xCC:
                self.__RaiseInterrupt(self.Breakpoint)
                continue

            else:
                ins = self.__FetchByte()

            if ins == MOV:
                self.__Ins_MOV(pre)

            elif ins == CALL:
                if pre & 0xF0 == Pre_64:
                    if pre & 0xF == Addr_Im:
                        value = self.__FetchQWord()
                        self.__PushByte(self.RIP)
                        self.RIP = value + self.RBP

            elif ins == JMP:
                if pre & 0xF0 == Pre_64:
                    if pre & 0xF == Addr_Im:
                        value = self.__FetchQWord()
                        self.RIP = value + self.RBP

            elif ins == PUSH:
                if pre & 0xF0 == Pre_64:
                    if pre & 0xF == Addr_Reg:
                        reg = self.__FetchByte()
                        self.__PushByte(self.__GetReg(reg, 0x64))

            elif ins == POP:
                if pre & 0xF0 == Pre_64:
                    if pre & 0xF == Addr_Reg:
                        reg = self.__FetchByte()
                        self.__SetReg(reg, self.__PopByte(), 0x64)

            else:
                self.__RaiseInterrupt(self.InvalidOpcode, opcode=ins)
