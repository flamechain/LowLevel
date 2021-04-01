from MTest import *
from Memory import Memory
from CPU import CPU
from InsCodes import *

const = 1

@runTest(-1+const)
def HelloWorld_SysWrite():
    memory = Memory(size=0xFFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x100] = ord("H")
    memory.Data[0x101] = ord("e")
    memory.Data[0x102] = ord("l")
    memory.Data[0x103] = ord("l")
    memory.Data[0x104] = ord("o")
    memory.Data[0x105] = ord(",")
    memory.Data[0x106] = ord(" ")
    memory.Data[0x107] = ord("w")
    memory.Data[0x108] = ord("o")
    memory.Data[0x109] = ord("r")
    memory.Data[0x10A] = ord("l")
    memory.Data[0x10B] = ord("d")
    memory.Data[0x10C] = ord("!")

    memory.Data[0x00] = MOV
    memory.Data[0x01] = Addr_RegIm8
    memory.Data[0x02] = Code_EAX
    memory.Data[0x03] = 4
    memory.Data[0x04] = MOV
    memory.Data[0x05] = Addr_RegIm8
    memory.Data[0x06] = Code_EBX
    memory.Data[0x07] = 1
    memory.Data[0x08] = MOV
    memory.Data[0x09] = Addr_RegIm16
    memory.Data[0x0A] = Code_ECX
    memory.Data[0x0B] = 0x01
    memory.Data[0x0C] = 0x00
    memory.Data[0x0D] = MOV
    memory.Data[0x0E] = Addr_RegIm8
    memory.Data[0x0F] = Code_EDX
    memory.Data[0x10] = 13

    memory.Data[0x11] = INT
    memory.Data[0x12] = 0x80

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(21 + 2 + 13)
    expect_eq(cycles, 21+2+13)

@runTest(-1+const)
def TestingSysExit():
    memory = Memory(size=0xFFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x0] = MOV
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = CPU.Sys_Exit
    memory.Data[0x4] = INT
    memory.Data[0x5] = 0x80

    cpu.LoadMemory(memory)
    cpu.Start()

@runTest(-1+const)
def InvalidOpcodeInterrupt():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x0] = 0xCD

    cpu.LoadMemory(memory)
    cpu.Start()

@runTest(-1+const)
def AddRegIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = ADD
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 2

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(6)
    expect_eq(cycles, 6)
    expect_eq(cpu.EAX, 5)

@runTest(-1+const)
def SUBRegIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = SUB
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 2

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(6)
    expect_eq(cycles, 6)
    expect_eq(cpu.EAX, 1)

@runTest(-1+const)
def DIVRegIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 4

    memory.Data[0x0] = DIV
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 2

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(6)
    expect_eq(cycles, 6)
    expect_eq(cpu.EAX, 2)

@runTest(-1+const)
def MULRegIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = MUL
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 2

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(6)
    expect_eq(cycles, 6)
    expect_eq(cpu.EAX, 6)

@runTest(-1+const)
def INCReg():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = INC
    memory.Data[0x1] = Addr_Reg
    memory.Data[0x2] = Code_EAX

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(5)
    expect_eq(cycles, 5)
    expect_eq(cpu.EAX, 4)

@runTest(-1+const)
def DECReg():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = DEC
    memory.Data[0x1] = Addr_Reg
    memory.Data[0x2] = Code_EAX

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(5)
    expect_eq(cycles, 5)
    expect_eq(cpu.EAX, 2)

@runTest(-1+const)
def CMPRegIm8Zero():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = CMP
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 3

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(5)
    expect_eq(cycles, 5)
    expect_eq(cpu.PS.Z, 1)

@runTest(-1+const)
def CMPRegIm8Pos():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = CMP
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 2

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(5)
    expect_eq(cycles, 5)
    expect_eq(cpu.PS.S, 0)

@runTest(-1+const)
def CMPRegIm8Neg():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.EAX = 3

    memory.Data[0x0] = CMP
    memory.Data[0x1] = Addr_RegIm8
    memory.Data[0x2] = Code_EAX
    memory.Data[0x3] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(5)
    expect_eq(cycles, 5)
    expect_eq(cpu.PS.S, 1)

@runTest(1)
def JMPIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x0] = JMP
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JEIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.PS.Z = 1

    memory.Data[0x0] = JE
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JNEIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x0] = JNE
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JGIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    memory.Data[0x0] = JG
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JGEIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.PS.Z = 1

    memory.Data[0x0] = JGE
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JLIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.PS.S = 1

    memory.Data[0x0] = JL
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

@runTest(1)
def JLEIm8():
    memory = Memory(size=0xFF)
    cpu = CPU()
    cpu.Debug = True

    cpu.PS.Z = 1

    memory.Data[0x0] = JLE
    memory.Data[0x1] = Addr_Im8
    memory.Data[0x2] = 4

    cpu.LoadMemory(memory)
    cycles = cpu.Execute(4)
    expect_eq(cycles, 4)
    expect_eq(cpu.PC, 4)

showTestResults()
