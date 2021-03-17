'''
CPU That handles all instructions. RISC system, current count is 98.

EMP32_5 CPU
'''
import time

from typing import Any

from Memory import Memory
from AllInstructions import *

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

class CPU:

    # Marked Locations
    IntLoc = 0xF0000
    COM0 = 0xF0001

    # Interupts
    reserved                   = 0x00
    SingleStepInterrupt        = 0x01
    NonMaskableInterrupt       = 0x02
    Breakpoint                 = 0x03
    Overflow                   = 0x04
    Bounds                     = 0x05
    InvalidOpcode              = 0x06
    CoprocessorNotAvailable    = 0x07
    DoubleFault                = 0x08
    CoprecessorSegmentOverrun  = 0x09
    InvalidTaskStateSegment    = 0x0A
    SegmentNotPresent          = 0x0B
    StackFault                 = 0x0C
    GeneralProtectionFault     = 0x0D
    PageFault                  = 0x0E
    DivideByZero               = 0x0F
    MathFault                  = 0x10
    AligmentCheck              = 0x11
    MachineCheck               = 0x12
    SIMDFloatingPointException = 0x13
    VirtualizationException    = 0x14
    ControlProtectionException = 0x15
    SysCall                    = 0x80

    # System Calls
    Sys_RestartSyscall = 0x00
    Sys_Exit           = 0x01
    Sys_Fork           = 0x02
    Sys_Read           = 0x03
    Sys_Write          = 0x04
    Sys_Open           = 0x05
    Sys_Close          = 0x06
    Sys_Time           = 0x0D
    Sys_fTime          = 0x23


    def __init__(self):
        '''CPU Instance that handles all instructions and has its own registers'''
        self.Memory = []
        self.PC = 0x00000000
        self.PS = Flags()
        self.Debug = False
        self.InInterupt = False
        self.Buffer = 0
        self.FileStart = 0xF000F
        self.FileDescriptors = {}

        self.EAO = 0x00000000
        self.EAX = 0x00000000
        self.EBX = 0x00000000
        self.ECX = 0x00000000
        self.EDX = 0x00000000
        self.ESI = 0x00000000
        self.EDI = 0x00000000
        self.EBP = 0x00000000
        self.ESP = 0x00000000
        self.AX  = 0x0000
        self.BX  = 0x0000
        self.CX  = 0x0000
        self.DX  = 0x0000
        self.BAX = 0x00
        self.BBX = 0x00
        self.BCX = 0x00
        self.BDX = 0x00

        self.Cycles = 0

    def LoadMemory(self, memory: Memory) -> None:
        '''Loads memory into interal storage, for faster access for the CPU'''
        self.Memory = memory.Data
        self.Buffer = len(self.Memory)

    def FireInterrupt(self) -> bool:
        '''Trigers a maskable interrupt'''
        self.PS.E = 1

    def __HandleSyscalls(self) -> None:
        '''Handles syscall interrupt'''
        if self.EAX == self.Sys_Write:
            if self.EBX == 1:
                string = ''
                counter = 0
                char = self.Memory[self.ECX]

                while counter < self.EDX:
                    string += chr(char)
                    counter += 1
                    char = self.Memory[self.ECX+counter]

                if self.Debug:
                    print("CPU: Interrupt: SysCall: Write: Out: %s" % string)

                else:
                    print(string, end='')

        elif self.EAX == self.Sys_Read:
            if self.EBX == 1:
                if self.Debug:
                    string = input("CPU: Interrupt: SysCall: Read: In [%s]: " % str(self.EDX))

                else:
                    string = input()

                for i in range(self.EDX):
                    try:
                        self.Memory[self.ECX+i] = ord(string[i])

                    except IndexError: break

        elif self.EAX == self.Sys_Exit:
            if self.EBX != 0:
                print("CPU: Interrupt: SysCall: Exit: %s" % hex(self.EBX))

            elif self.Debug:
                print("CPU: Interrupt: SysCall: Exit: %s" % hex(self.EBX))

            raise Exception('')

        elif self.EAX == self.Sys_Open:
            filename = ''
            counter = 0
            char = self.Memory[self.EBX]

            while char != 0:
                filename += chr(char)
                counter += 1
                char = self.Memory[self.EBX+counter]

            try:
                with open(filename, 'r') as f:
                    string = f.read()

            except:
                self.__RaiseError(self.SegmentNotPresent)

            for i in range(self.ECX):
                try:
                    self.Memory[self.FileStart+i] = ord(string[i])

                except IndexError: break

            self.FileDescriptors[filename] = self.FileStart
            self.FileStart += self.ECX

        elif self.EAX == self.Sys_Time:
            time_t = int(time.time())

            self.EAX = time_t

            if self.EBX != 0:
                self.__WriteDWord(self.EBX, time_t)

    def __HandleInterrupt(self) -> None:
        '''Hanldes all interrupts'''
        if self.Memory[self.IntLoc] == self.SysCall:
            self.__HandleSyscalls()

        self.InInterupt = False
        self.PS.E = 0

    def __RaiseInterrupt(self, code: int, **kwargs) -> bool:
        '''Raises interrupts'''
        try:
            string = 'CPU: Interrupt: '

            if code == self.SingleStepInterrupt:
                string += 'SingleStepInterrupt: %s' % hex(self.PC)
                input(string)
                return

            elif code == self.NonMaskableInterrupt:
                string += 'NonMaskableInterrupt: %s' % hex(self.PC)

            elif code == self.Breakpoint:
                string += 'Breakpoint: %s' % hex(self.PC)
                input(string)
                return

            elif code == self.Overflow:
                string += 'Overflow: %s' % hex(self.PC)

            elif code == self.Bounds:
                string += 'Bounds: %s' % hex(self.PC)

            elif code == self.InvalidOpcode:
                string += 'InvalidOpcode: %s at %s' % (hex(kwargs['opcode']), hex(self.PC))

            elif code == self.CoprocessorNotAvailable:
                string += 'CoprocessorNotAvailable: %s, CPUID: ' % (hex(self.PC), hex(kwargs['cpuid']))

            elif code == self.InvalidTaskStateSegment:
                string += 'InvalidTaskStateSegment: %s' % hex(self.PC)

            elif code == self.SegmentNotPresent:
                string += 'SegmentNotPresent: %s' % hex(self.PC)

            elif code == self.InvalidTaskStateSegment:
                string += 'InvalidTaskStateSegment: %s' % hex(self.PC)

            elif code == self.StackFault:
                string += 'StackFault: %s' % hex(self.PC)

            elif code == self.GeneralProtectionFault:
                string += 'GeneralProtectionFault: %s' % hex(self.PC)

            elif code == self.PageFault:
                string += 'PageFault: %s' % hex(self.PC)

            elif code == self.DivideByZero:
                string += 'DivideByZero: %s' % hex(self.PC)

            elif code == self.MathFault:
                string += 'MathFault: %s' % hex(self.PC)

            elif code == self.SIMDFloatingPointException:
                string += 'SIMDFloatingPointException: %s' % hex(self.PC)

            elif code == self.VirtualizationException:
                string += 'VirtualizationException: %s' % hex(self.PC)

            elif code == self.ControlProtectionException:
                string += 'ControlProtectionException: %s' % hex(self.PC)

        except Exception as e:
            if self.Debug:
                print("CPU: Interrupt: DoubleFault: Origin: %s" % e)

            raise Exception(string + 'DoubleFault: %s' % hex(self.PC))

        raise Exception(string)

    def __CheckForInterrupts(self) -> None:
        '''Checks for external interrupts'''
        if not self.PS.I:
            if not self.InInterupt:
                if self.PS.E:
                    self.InInterupt = True
                    self.__HandleInterrupt()

    def __FetchByte(self) -> int:
        '''Gets next byte from memory'''
        if self.PC >= self.Buffer:
            self.__RaiseInterrupt(self.SegmentNotPresent)

        value = self.Memory[self.PC]
        self.PC += 1
        self.Cycles -= 1

        return value

    def __FetchWord(self) -> int:
        '''Gets next word from memory'''
        return self.__FetchByte() << 8 | self.__FetchByte()

    def __FetchDWord(self) -> int:
        '''Gets next double word from memory'''
        return self.__FetchWord() << 16 | self.__FetchWord()

    def __ReadByte(self, address) -> int:
        '''Reads a byte from memory'''
        return self.Memory[address]

    def __ReadWord(self, address) -> int:
        '''Reads a word from memory'''
        return self.__ReadByte(address) << 8 | self.__ReadByte(address+1)

    def __ReadDWord(self, address) -> int:
        '''Reads a double word from memory'''
        return self.__ReadWord(address) << 16 | self.__ReadWord(address+2)

    def __WriteDWord(self, address: int, value: int) -> None:
        '''Writes a double word to memory'''
        self.Memory[address] = (value & 0xFF000000) >> 24
        self.Memory[address+1] = (value & 0xFF0000) >> 16
        self.Memory[address+2] = (value & 0xFF00) >> 8
        self.Memory[address+3] = value & 0xFF
        self.Cycles -= 4

    def __SetReg(self, code: int, value: int) -> None:
        '''Sets a register based of registers codes'''
        if code == Code_EAX:
            self.EAX = value

        elif code == Code_EBX:
            self.EBX = value

        elif code == Code_ECX:
            self.ECX = value

        elif code == Code_EDX:
            self.EDX = value

    def Start(self) -> None:
        if not self.Debug:
            try:
                self.Execute('inf')

            except Exception as e:
                print(e)
                return

        else:
            self.Execute('inf')

    def Execute(self, cycles: int) -> Any:
        '''Executes from memory 0x0 until all cycles are consumed'''
        if cycles == 'inf':
            self.Cycles = 1

        else:
            self.Cycles = cycles

        while (self.Cycles > 0) or (cycles == 'inf'):
            self.__CheckForInterrupts()

            if self.PS.T:
                self.__RaiseInterrupt(self.SingleStepInterupt)

            ins = self.__FetchByte()

            if ins == ABS:
                pass

            elif ins == INC:
                mod = self.__FetchByte()

                if mod == Addr_Disp16:
                    address = self.__FetchWord()
                    value = self.__ReadDWord(address)
                    value += 1
                    self.__WriteDWord(address, value)

            elif ins == JMPAHD:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    value = self.__FetchByte()
                    self.PC += value

            elif ins == NOP:
                pass

            elif ins == MOV:
                mod = self.__FetchByte()

                if mod == Addr_RegIm8:
                    reg = self.__FetchByte()
                    im = self.__FetchByte()
                    self.__SetReg(reg, im)

                elif mod == Addr_RegIm16:
                    reg = self.__FetchByte()
                    im = self.__FetchWord()
                    self.__SetReg(reg, im)

                elif mod == Addr_RegIm32:
                    reg = self.__FetchByte()
                    im = self.__FetchDWord()
                    self.__SetReg(reg, im)

            elif ins == INT:
                intCode = self.__FetchByte()
                self.Memory[self.IntLoc] = intCode
                self.__HandleInterrupt()

            elif ins == CMP:
                mod = self.__FetchByte()

                if mod == Addr_Disp16Disp16:
                    address1 = self.__FetchWord()
                    address2 = self.__FetchWord()
                    value1 = self.__ReadDWord(address1)
                    value2 = self.__ReadDWord(address2)
                    result = value1 - value2

                    if result == 0:
                        self.PS.Z = 1

                    elif result < 0:
                        self.PS.S = 1

            elif ins == JNE:
                mod = self.__FetchByte()

                if mod == Addr_Im8:
                    address = self.__FetchByte()

                    if not self.PS.Z:
                        self.PC = address + self.EAO

            elif ins == 0xCC:
                self.__RaiseInterrupt(self.Breakpoint)

            else:
                self.__RaiseInterrupt(self.InvalidOpcode, opcode=ins)
                return

        if self.Debug:
            ret = cycles - self.Cycles

        else:
            ret = None

        return ret
