from CPU import *
from MyTest import *

settings.stopOnFirstFail = False

@group('cpu')
@test()
def TEST_PC_Init():
    cpu = CPU()
    EXPECT_EQ(cpu.PC, (cpu.memory.Data[0xFFFC] << 8) | (cpu.memory.Data[0xFFFD]))

@group('cpu')
@test()
def TEST_PC_Wrapping():
    cpu = CPU()
    cpu.PC = Byte(0b1111111111111111)
    cpu.PC += 1
    EXPECT_EQ(cpu.PC, 0b0)
    cpu.PC = Byte(0b0)
    cpu.PC -= 1
    EXPECT_EQ(cpu.PC, 0b1111111111111111)

@group('cpu')
@test()
def TEST_InvalidOpcode():
    cpu = CPU()
    cpu.memory.Data[0xFF00] = 0x33
    EXPECT_ERROR(cpu.Execute, params=1, expectedErrors=[Exception])

@group('nop')
@test()
def TEST_NOP():
    cpu = CPU()
    cpu.memory.Data[0xFF00] = cpu.INS_NOP
    CyclesUsed = cpu.Execute(1)
    EXPECT_EQ(CyclesUsed, 1)

@group('ldac')
@test()
def TEST_LDAC_IM():
    cpu = CPU()
    cpu.memory.Data[0xFF00] = cpu.INS_LDAC_IM
    cpu.memory.Data[0xFF01] = 0x42
    CyclesUsed = cpu.Execute(3)
    EXPECT_EQ(cpu.A, 0x42)
    EXPECT_EQ(CyclesUsed, 3)

@group('stac')
@test()
def TEST_STAC_ABS():
    cpu = CPU()
    cpu.memory.Data[0xFF00] = cpu.INS_STAC_ABS
    cpu.memory.Data[0xFF01] = 0x42
    cpu.A = 0x80
    CyclesUsed = cpu.Execute(4)
    EXPECT_EQ(cpu.memory.Data[0x4200], 0x80)
    EXPECT_EQ(CyclesUsed, 4)

@group('jmp')
@test()
def TEST_JMP_ABS():
    cpu = CPU()
    cpu.memory.Data[0xFF00] = cpu.INS_JMP_ABS
    cpu.memory.Data[0xFF02] = 0x42
    CyclesUsed = cpu.Execute(3)
    EXPECT_EQ(cpu.PC, 0x0042)
    EXPECT_EQ(CyclesUsed, 3)

@group('manual')
@test()
def TEST_TrapFlag():
    cpu = CPU()
    cpu.T = 1
    cpu.UpdatePS()
    cpu.memory.Data[0xFF00] = cpu.INS_NOP
    cpu.memory.Data[0xFF01] = cpu.INS_NOP
    CyclesUsed = cpu.Execute(2)
    EXPECT_EQ(CyclesUsed, 2)

@group('ror')
@test()
def TEST_ROR_AC():
    cpu = CPU()
    cpu.A = 0x42
    cpu.memory.Data[0xFF00] = cpu.INS_ROR_AC
    CyclesUsed = cpu.Execute(3)
    EXPECT_EQ(CyclesUsed, 3)
    EXPECT_EQ(cpu.A, 0x21)

@group('prg')
@test()
def TEST_PRG_1():
    cpu = CPU(reset_vector=0x8000)
    cpu.memory.Data[0x8000] = cpu.INS_LDAC_IM
    cpu.memory.Data[0x8001] = 0xFF
    cpu.memory.Data[0x8002] = cpu.INS_STAC_ABS
    cpu.memory.Data[0x8003] = 0x60
    cpu.memory.Data[0x8004] = 0x02
    cpu.memory.Data[0x8005] = cpu.INS_LDAC_IM
    cpu.memory.Data[0x8006] = 0x55
    cpu.memory.Data[0x8007] = cpu.INS_STAC_ABS
    cpu.memory.Data[0x8008] = 0x60
    # cpu.memory.Data[0x8009] = 0x00
    cpu.memory.Data[0x800A] = cpu.INS_LDAC_IM
    cpu.memory.Data[0x800B] = 0xAA
    cpu.memory.Data[0x800C] = cpu.INS_STAC_ABS
    cpu.memory.Data[0x800D] = 0x60
    # cpu.memory.Data[0x800E] = 0x00
    cpu.memory.Data[0x800F] = cpu.INS_JMP_ABS
    cpu.memory.Data[0x8010] = 0x80
    cpu.memory.Data[0x8011] = 0x05
    CyclesUsed = cpu.Execute(18)
    EXPECT_EQ(cpu.A, 0xAA)
    EXPECT_EQ(cpu.memory.Data[0x6002], 0xFF)
    EXPECT_EQ(cpu.memory.Data[0x6000], 0xAA)
    EXPECT_EQ(CyclesUsed, 18)

@group('prg2')
@test()
def TEST_LOADPRG():
    cpu = CPU()
    with open('a.out', 'r') as f:
        prg = f.read()
    cpu.LoadProgram(prg)
    CyclesUsed = cpu.Execute(24)
    EXPECT_EQ(CyclesUsed, 24)
    EXPECT_EQ(cpu.A, 0x28)
    EXPECT_EQ(cpu.memory.Data[0x6000], cpu.A)


# runTests(exclude=['manual', 'framework', 'prg'])
runTests(toRun=['prg2'])
showTestResults()
