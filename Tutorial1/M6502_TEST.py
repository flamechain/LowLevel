'''
Testing for my 6502 CPU Emulator.

This uses a custom testing framework.
'''

from M6502 import *
import termcolor
import time
import inspect

# Global Variables

total = 0
done = 0
success = 0
failed = 0
equates = {}
start = time.time()

# Logging Level
level = 0

# Testing Framework

def runTest(priorety=0):
    '''Handles equate_* statements for each test'''
    def inner(func):
        def wrapper(*args, **kwargs):
            global success, failed, total, done, equates, level
            if priorety >= level:

                total += 1
                done += 1
                plus = termcolor.colored('+', 'green')
                minus = termcolor.colored('-', 'red')

                try:
                    func()

                    for i in equates:
                        if equates[i] == False:
                            failed += 1
                            print('[%s] Function %s failed.' % (minus, func.__name__))
                            for j in equates:
                                if equates[j] == False:
                                    print('    %s %s' % (termcolor.colored('Failed expect_eq:', 'red'), j))
                            equates = {}

                            return

                    success += 1
                    print('[%s] Function %s succeded.' % (plus, func.__name__))

                except Exception as e:
                    done -= 1
                    print('[%s] Function %s %s\n    %s %s' % (minus, func.__name__, termcolor.colored('failed to execute.', 'red'),termcolor.colored('Raised Exception:', 'red'), e))

                equates = {}
        return wrapper()
    return inner

def showTestResults():
    global success, failed, total, done

    end = time.time()
    runtime = round(end-start, 2)
    testssuccess = '%d tests succeded' % success
    outof = 'out of'
    failnum = failed
    failed = '%d tests failed' % failed
    if success == total:
        testssuccess = termcolor.colored(testssuccess, 'green')
    if done < total:
        done = termcolor.colored(str(done), 'red')
        total = termcolor.colored(str(total), 'red')
        outof = termcolor.colored(outof, 'red')
    if failnum > 0:
        failed = termcolor.colored(failed, 'red')

    print('\nTest Results:\n\nRan %s %s %s tests.    \n--------------------------------------\n    %s\n    %s\n\n    Total Runtime: %ss\n--------------------------------------' % (done, outof, total, testssuccess, failed, str(runtime)))

def expect_eq(a, b):
    '''Stores result in list'''
    global equates

    if a == b:
        equates[str(a) + str(b) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []
        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())
            else:
                names.append(i)
        if names[1].startswith(' '):
            names[1] = names[1][1:]
        equates[f'{a} != {b} ({names[0]}, {names[1]})'] = False


# Tests


def checkLDFlags(cpu, copy):
    expect_eq(cpu.C, copy.C)
    expect_eq(cpu.I, copy.I)
    expect_eq(cpu.D, copy.D)
    expect_eq(cpu.B, copy.B)
    expect_eq(cpu.V, copy.V)

def checkAllFlags(cpu, copy):
    expect_eq(cpu.N, copy.N)
    expect_eq(cpu.Z, copy.Z)
    expect_eq(cpu.C, copy.C)
    expect_eq(cpu.I, copy.I)
    expect_eq(cpu.D, copy.D)
    expect_eq(cpu.B, copy.B)
    expect_eq(cpu.V, copy.V)

def checkPS(cpu, copy):
    expect_eq(cpu.PC, copy.PC)
    expect_eq(cpu.N, copy.N)
    expect_eq(cpu.Z, copy.Z)
    expect_eq(cpu.C, copy.C)
    expect_eq(cpu.I, copy.I)
    expect_eq(cpu.D, copy.D)
    expect_eq(cpu.B, copy.B)
    expect_eq(cpu.V, copy.V)


# LDA

@runTest()
def TEST_UseExtraCyclesIfRequired():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_LDA_IM
    mem.Data[0xFFFD] = 0x84
    CyclesUsed = cpu.Execute(1, mem)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ZeroCPUCycles():
    mem = Mem()
    cpu = CPU()
    CyclesUsed = cpu.Execute(0, mem)
    expect_eq(CyclesUsed, 0)

@runTest()
def TEST_LDA_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_IM
    mem.Data[0xFFFD] = 0x84
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x84)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ZPX_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x44
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ABSX_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSY
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4485] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_ABSY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 0x37
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 0x37
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDA_INDY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x02
    mem.Data[0x0003] = 0x80
    mem.Data[0x8101] = 0x50
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)


# LDX


@runTest()
def TEST_LDX_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDX_IM
    mem.Data[0xFFFD] = 0x50
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.X, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.Y, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ZPY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ZPY_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x44
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDX_ABSY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)


# LDY


@runTest()
def TEST_LDY_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_IM
    mem.Data[0xFFFD] = 0x50
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Y, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.Y, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ZPX_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x44
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDY_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_LDY_ABSX_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_LDA_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)


# STA


@runTest()
def TEST_STA_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STA_ZP
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(mem.Data[0x0080], 0x2F)
    expect_eq(CyclesUsed, 3)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STA_ABS
    mem.Data[0xFFFD] = 0x0
    mem.Data[0xFFFE] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x8000], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xF
    cpu.A = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STA_ZPX
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x008F], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xF
    cpu.A = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STA_ABSX
    mem.Data[0xFFFD] = 0x00
    mem.Data[0xFFFE] = 0x80
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x800F], 0x2F)
    expect_eq(CyclesUsed, 5)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xF
    cpu.A = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STA_ABSY
    mem.Data[0xFFFD] = 0x00
    mem.Data[0xFFFE] = 0x80
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x800F], 0x2F)
    expect_eq(CyclesUsed, 5)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xF
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_STA_INDX
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x002F] = 0x00
    mem.Data[0x0030] = 0x80
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x8000], 0x42)
    expect_eq(CyclesUsed, 6)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STA_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xF
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_STA_INDY
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x00
    mem.Data[0x0021] = 0x80
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x800F], 0x42)
    expect_eq(CyclesUsed, 6)
    checkAllFlags(cpu, cpuCopy)


# STX


@runTest()
def TEST_STX_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STX_ZP
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(mem.Data[0x0080], 0x2F)
    expect_eq(CyclesUsed, 3)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STX_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STX_ABS
    mem.Data[0xFFFD] = 0x00
    mem.Data[0xFFFE] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x8000], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STX_ZPY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xF
    cpu.X = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STX_ZPY
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x008F], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)


# STY


@runTest()
def TEST_STY_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STY_ZP
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(mem.Data[0x0080], 0x2F)
    expect_eq(CyclesUsed, 3)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STY_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STY_ABS
    mem.Data[0xFFFD] = 0x00
    mem.Data[0xFFFE] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x8000], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)

@runTest()
def TEST_STY_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xF
    cpu.Y = 0x2F
    mem.Data[0xFFFC] = cpu.INS_STY_ZPX
    mem.Data[0xFFFD] = 0x80
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(mem.Data[0x008F], 0x2F)
    expect_eq(CyclesUsed, 4)
    checkAllFlags(cpu, cpuCopy)


# JMP


@runTest()
def TEST_JMP_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_JMP_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.SP, cpuCopy.SP)
    expect_eq(cpu.PC, 0x8000)

@runTest()
def TEST_JMP_IND():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_JMP_IND
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 0x00
    mem.Data[0x8001] = 0x90
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(CyclesUsed, 5)
    expect_eq(cpu.SP, cpuCopy.SP)
    expect_eq(cpu.PC, 0x9000)


# JSR & RTS


@runTest()
def TEST_JSR_RTS_wLDA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_JSR
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = cpu.INS_RTS
    mem.Data[0xFF03] = cpu.INS_LDA_IM
    mem.Data[0xFF04] = 0x42
    CyclesUsed = cpu.Execute(14, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(CyclesUsed, 14)
    expect_eq(cpu.SP, cpuCopy.SP)

@runTest()
def TEST_JSR_RTS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_JSR
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = cpu.INS_RTS
    CyclesUsed = cpu.Execute(12, mem)
    expect_eq(CyclesUsed, 12)
    expect_eq(cpu.SP, cpuCopy.SP)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_JSR_AffectPC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_JSR
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    checkPS(cpu, cpuCopy)


# TSX


@runTest()
def TEST_TSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.SP = 0x1
    mem.Data[0xFF00] = cpu.INS_TSX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, cpu.SP)
    checkPS(cpu, cpuCopy)

@runTest()
def TEST_TSX_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpuCopy.Z = 1
    cpu.SP = 0x0
    mem.Data[0xFF00] = cpu.INS_TSX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, cpu.SP)
    checkPS(cpu, cpuCopy)

@runTest()
def TEST_TSX_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpuCopy.N = 1
    cpu.SP = 0b10000000
    mem.Data[0xFF00] = cpu.INS_TSX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, cpu.SP)
    checkPS(cpu, cpuCopy)


# TXS


@runTest()
def TEST_TXS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.SP = 0x00
    mem.Data[0xFF00] = cpu.INS_TXS
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, cpu.SP)
    checkPS(cpu, cpuCopy)


# PHA


@runTest()
def TEST_PHA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.A = 0x42
    mem.Data[0xFF00] = cpu.INS_PHA
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(mem.Data[cpu.SPToAddress()+1], cpu.A)
    checkPS(cpu, cpuCopy)

@runTest()
def TEST_PHA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.A = 0x42
    mem.Data[0xFF00] = cpu.INS_PHA
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(mem.Data[cpu.SPToAddress()+1], cpu.A)
    checkPS(cpu, cpuCopy)


# PHP


@runTest(1)
def TEST_PHP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.PS = 0xCC
    cpu.PSToPSL()
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_PHP
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(mem.Data[cpu.SPToAddress()+1], 0xCC)
    expect_eq(cpu.PS, cpuCopy.PS)
    expect_eq(cpu.SP, 0xFE)

@runTest(1)
def TEST_PHP_Bit45():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.PS = 0xCC
    cpu.PSToPSL()
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_PHP
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    cpu.Unused = 1
    cpu.B = 1
    cpu.Z = cpu.C = cpu.D = cpu.I = cpu.V = cpu.N = 0
    cpu.UpdatePS()
    expect_eq(mem.Data[cpu.SPToAddress()+1], cpu.PS)


# PLA


@runTest()
def TEST_PLA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.SP = 0xFE
    cpuCopy = cpu
    mem.Data[0x01FF] = 0x42
    mem.Data[0xFF00] = cpu.INS_PLA
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(CyclesUsed, 4)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.PS, cpuCopy.PS)
    expect_eq(cpu.SP, 0xFF)

@runTest()
def TEST_PLA_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.SP = 0xFE
    cpu.A = 0x42
    mem.Data[0x01FF] = 0x0
    mem.Data[0xFF00] = cpu.INS_PLA
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(CyclesUsed, 4)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.Z, 1)

@runTest()
def TEST_PLA_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.SP = 0xFE
    cpu.A = 0x42
    mem.Data[0x01FF] = -0x1
    mem.Data[0xFF00] = cpu.INS_PLA
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(CyclesUsed, 4)
    expect_eq(cpu.A, -0x1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.SP, 0xFF)


# PLP


@runTest()
def TEST_PLP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.SP = 0xFE
    cpu.PS = 0x0
    cpu.PSToPSL()
    cpuCopy = cpu
    mem.Data[0x01FF] = 0x42
    mem.Data[0xFF00] = cpu.INS_PLP
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(CyclesUsed, 4)
    expect_eq(cpu.PS, 0x42)
    expect_eq(cpu.SP, 0xFF)


# AND


@runTest()
def TEST_AND_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    cpu.A = 0x84
    mem.Data[0xFFFC] = cpu.INS_AND_IM
    mem.Data[0xFFFD] = 0x84
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x84)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    cpu.A = 0x37
    mem.Data[0xFFFC] = cpu.INS_AND_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    cpu.A = 0x24
    mem.Data[0xFFFC] = cpu.INS_AND_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ZPX_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    cpu.A = 0x21
    mem.Data[0xFFFC] = cpu.INS_AND_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.A = 0x44
    cpu.Z = cpu.N = 1
    cpu.A = 0xFF
    mem.Data[0xFFFC] = cpu.INS_AND_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    cpu.A = 0x32
    mem.Data[0xFFFC] = cpu.INS_AND_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    cpu.A = 0x89
    mem.Data[0xFFFC] = cpu.INS_AND_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ABSX_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.A = 0x89
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_AND_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x5
    cpu.Z = cpu.N = 1
    cpu.A = 0x89
    mem.Data[0xFFFC] = cpu.INS_AND_ABSY
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4485] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_ABSY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    cpu.A = 0x89
    mem.Data[0xFFFC] = cpu.INS_AND_ABSY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x04
    cpu.Z = cpu.N = 1
    cpu.A = 0x37
    mem.Data[0xFFFC] = cpu.INS_AND_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 0x37
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x04
    cpu.A = 0x37
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_AND_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 0x37
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_AND_INDY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.A = 0x50
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_AND_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x02
    mem.Data[0x0003] = 0x80
    mem.Data[0x8101] = 0x50
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)


# EOR


@runTest()
def TEST_EOR_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_IM
    mem.Data[0xFFFD] = 0x84
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x84)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ZPX_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ABSX_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ABSY
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4485] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_ABSY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_ABSY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 0x37
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 0x37
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_EOR_INDY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_EOR_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x02
    mem.Data[0x0003] = 0x80
    mem.Data[0x8101] = 0x50
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)


# ORA


@runTest()
def TEST_ORA_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_IM
    mem.Data[0xFFFD] = 0x84
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x84)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 2)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x37
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 3)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x24
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x24)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)    
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ZPX_WhenWrap():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ZPX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0x007F] = 0x21
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x21)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_IM_AffectZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ABS
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4480] = 0x32
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x32)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x1
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ABSX
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4481] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ABSX_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ABSX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x5
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ABSY
    mem.Data[0xFFFD] = 0x80
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4485] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 4)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_ABSY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_ABSY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0xFFFE] = 0x44
    mem.Data[0x4501] = 0x89
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.X = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 0x37
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0x04
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 0x37
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0x37)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 5)
    checkLDFlags(cpu, cpuCopy)

@runTest()
def TEST_ORA_INDY_WhenPageCross():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    cpu.Y = 0xFF
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_ORA_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x02
    mem.Data[0x0003] = 0x80
    mem.Data[0x8101] = 0x50
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x50)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)
    checkLDFlags(cpu, cpuCopy)


# BIT


@runTest()
def TEST_BIT_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0xCC
    cpu.N = 0
    mem.Data[0xFFFC] = cpu.INS_BIT_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0xCC
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.A, 0xCC)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.V, 1)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_BIT_ZeroFlag():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = 1
    cpu.A = 0xCC
    mem.Data[0xFFFC] = cpu.INS_BIT_ZP
    mem.Data[0xFFFD] = 0x42
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.A, 0xCC)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_BIT_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0xCC
    cpu.N = 0
    mem.Data[0xFFFC] = cpu.INS_BIT_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x00
    mem.Data[0x0042] = 0xCC
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(CyclesUsed, 4)
    expect_eq(cpu.A, 0xCC)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.V, 1)
    expect_eq(cpu.N, 1)


# TAX, TAY, TXA, TYA


@runTest()
def TEST_TAX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    cpu.X = 0x32
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TAX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.X, 0x42)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TAX_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x0
    cpu.X = 0x32
    cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TAX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.X, 0x0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TAX_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x89
    cpu.X = 0x32
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_TAX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.X, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_TAY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    cpu.Y = 0x32
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TAY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Y, 0x42)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TAY_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x0
    cpu.Y = 0x32
    cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TAY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.Y, 0x0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TAY_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x89
    cpu.Y = 0x32
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_TAY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Y, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_TXA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.X = 0x42
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TXA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.X, 0x42)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TXA_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.X = 0x0
    cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TXA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.X, 0x0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TXA_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.X = 0x89
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_TXA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.X, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_TYA():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.Y = 0x42
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TYA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Y, 0x42)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TYA_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.Y = 0x0
    cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_TYA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.Y, 0x0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_TYA_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x32
    cpu.Y = 0x89
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_TYA
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.A, 0x89)
    expect_eq(cpu.Y, 0x89)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)


# INX, INY, DEX, DEY


@runTest()
def TEST_INX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_INX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INX_Overflow():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    cpu.X = 0xFF
    mem.Data[0xFFFC] = cpu.INS_INX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_INY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.Y, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INY_Overflow():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    cpu.Y = 0xFF
    mem.Data[0xFFFC] = cpu.INS_INY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.Y, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_DEX_Underflow():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_DEX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, 0xFF)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_DEX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    cpu.X = 0xFF
    mem.Data[0xFFFC] = cpu.INS_DEX
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.X, 0xFE)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_DEY_Underflow():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_DEY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.Y, 0xFF)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)

@runTest()
def TEST_DEY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.N = cpu.Z = 1
    cpu.Y = 0xFF
    mem.Data[0xFFFC] = cpu.INS_DEY
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.Y, 0xFE)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)


# DEC


@runTest()
def TEST_DEC_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_DEC_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x57
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(CyclesUsed, 5)
    expect_eq(mem.Data[0x0042], 0x56)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_DEC_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    cpu.X = 0x5
    mem.Data[0xFFFC] = cpu.INS_DEC_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x57
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    expect_eq(mem.Data[0x0047], 0x56)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_DEC_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_DEC_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x00
    mem.Data[0x0042] = 0x57
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    expect_eq(mem.Data[0x0042], 0x56)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_DEC_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    cpu.X = 0x5
    mem.Data[0xFFFC] = cpu.INS_DEC_ABSX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x00
    mem.Data[0x0047] = 0x57
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(CyclesUsed, 7)
    expect_eq(mem.Data[0x0047], 0x56)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)


# INC


@runTest()
def TEST_INC_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_INC_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0x57
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(CyclesUsed, 5)
    expect_eq(mem.Data[0x0042], 0x58)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INC_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    cpu.X = 0x5
    mem.Data[0xFFFC] = cpu.INS_INC_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0047] = 0x57
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    expect_eq(mem.Data[0x0047], 0x58)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INC_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    mem.Data[0xFFFC] = cpu.INS_INC_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x00
    mem.Data[0x0042] = 0x57
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    expect_eq(mem.Data[0x0042], 0x58)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)

@runTest()
def TEST_INC_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = cpu.N = 1
    cpu.X = 0x5
    mem.Data[0xFFFC] = cpu.INS_INC_ABSX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x00
    mem.Data[0x0047] = 0x57
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(CyclesUsed, 7)
    expect_eq(mem.Data[0x0047], 0x58)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)


# BCC, BCS, BEQ, BMI, BNE, BPL, BVS, BVC


@runTest()
def TEST_BEQ():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Z = 1
    mem.Data[0xFFFC] = cpu.INS_BEQ
    mem.Data[0xFFFD] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFFFF)

@runTest()
def TEST_BEQ_NoZero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_BEQ
    mem.Data[0xFFFD] = 0x1
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.PC, 0xFFFE)

@runTest()
def TEST_BEQ_NextPage():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFEFD)
    cpu.Z = 1
    mem.Data[0xFEFD] = cpu.INS_BEQ
    mem.Data[0xFEFE] = 0x1
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(CyclesUsed, 5)
    expect_eq(cpu.PC, 0xFF00)

@runTest()
def TEST_BEQ_Backwards():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFFCC)
    cpu.Z = 1
    mem.Data[0xFFCC] = cpu.INS_BEQ
    mem.Data[0xFFCD] = -0x3
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFFCB)

@runTest()
def TEST_BEQ_NoZero_Backwards():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFFCC)
    mem.Data[0xFFCC] = cpu.INS_BEQ
    mem.Data[0xFFCD] = -0x3
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.PC, 0xFFCE)

@runTest()
def TEST_BEQ_CheckAssembler():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFFCC)
    cpu.Z = 1
    mem.Data[0xFFCC] = 0xA9
    mem.Data[0xFFCC+1] = 0x00
    mem.Data[0xFFCC+2] = 0xF0
    mem.Data[0xFFCC+3] = 0xFC
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(CyclesUsed, 5)
    expect_eq(cpu.PC, 0xFFCC)

@runTest()
def TEST_BNE():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    mem.Data[0xFF00] = cpu.INS_BNE
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BCS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_BCS
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BCC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    mem.Data[0xFF00] = cpu.INS_BCC
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BMI():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.N = 1
    mem.Data[0xFF00] = cpu.INS_BMI
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BPL():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    mem.Data[0xFF00] = cpu.INS_BPL
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BVS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.V = 1
    mem.Data[0xFF00] = cpu.INS_BVS
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)

@runTest()
def TEST_BVC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    mem.Data[0xFF00] = cpu.INS_BVC
    mem.Data[0xFF01] = 0x1
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(CyclesUsed, 3)
    expect_eq(cpu.PC, 0xFF03)


# CLC, CLD, CLI, CLV, SEC, SED, SEI


@runTest()
def TEST_CLC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.C = 1
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_CLC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, cpuCopy.I)
    expect_eq(cpu.D, cpuCopy.D)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_SEC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_SEC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, cpuCopy.I)
    expect_eq(cpu.D, cpuCopy.D)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_CLD():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.D = 1
    mem.Data[0xFF00] = cpu.INS_CLD
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, cpuCopy.C)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, cpuCopy.I)
    expect_eq(cpu.D, 0)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_CLI():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.I = 1
    mem.Data[0xFF00] = cpu.INS_CLI
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, cpuCopy.C)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, 0)
    expect_eq(cpu.D, cpuCopy.D)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_CLV():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    cpu.V = 1
    mem.Data[0xFF00] = cpu.INS_CLV
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, cpuCopy.C)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, cpuCopy.I)
    expect_eq(cpu.D, cpuCopy.D)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_SED():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_SED
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, cpuCopy.C)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, cpuCopy.I)
    expect_eq(cpu.D, 1)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)

@runTest()
def TEST_SEI():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_SEI
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.C, cpuCopy.C)
    expect_eq(cpu.Z, cpuCopy.Z)
    expect_eq(cpu.I, 1)
    expect_eq(cpu.D, cpuCopy.D)
    expect_eq(cpu.B, cpuCopy.B)
    expect_eq(cpu.V, cpuCopy.V)
    expect_eq(cpu.N, cpuCopy.N)


# NOP


@runTest()
def TEST_NOP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpuCopy = cpu
    mem.Data[0xFF00] = cpu.INS_NOP
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(CyclesUsed, 2)
    expect_eq(cpu.PS, cpuCopy.PS)
    expect_eq(cpu.PC, 0xFF01)


# ADC


@runTest()
def TEST_ADC_ABS_ZeroPZero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.V = cpu.N = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 0x00
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_ZeroPZeroPCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.C = cpu.V = cpu.N = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 0x00
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x1)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_FFPOnePCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0xFF
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 0x01
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_ZeroPnOnePCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0x0
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = -0x1
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, -0x1)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_MaxNegative():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = -0b10000000
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = -0x1
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 127)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_MaxNegative_wCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = -0b10000000
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = -0x1
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, -128)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_MaxPositive():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 127
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 0x1
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 128)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_Normal():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 17
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_NormalSigned():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = -17
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 4)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABS_NormalSigned2():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = -2
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ABS
    mem.Data[0xFF01] = 0x00
    mem.Data[0xFF02] = 0x80
    mem.Data[0x8000] = 2
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 1)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_IM
    mem.Data[0xFF01] = 17
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ADC_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_ADC_ZP
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0042] = 17
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 3)

@runTest()
def TEST_ADC_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    cpu.X = 5
    mem.Data[0xFF00] = cpu.INS_ADC_ZPX
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 17
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    cpu.X = 5
    mem.Data[0xFF00] = cpu.INS_ADC_ABSX
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 17
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 20
    cpu.C = 1
    cpu.Y = 5
    mem.Data[0xFF00] = cpu.INS_ADC_ABSY
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 17
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 38)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_ADC_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 0x04
    cpu.A = 20
    mem.Data[0xFFFC] = cpu.INS_ADC_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 17
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 37)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ADC_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 20
    cpu.Y = 0x04
    mem.Data[0xFFFC] = cpu.INS_ADC_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 17
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 37)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 5)


# CMP


@runTest()
def TEST_CMP_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_IM
    mem.Data[0xFFFD] = 0x42
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CMP_IM_Pos():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x48
    mem.Data[0xFFFC] = cpu.INS_CMP_IM
    mem.Data[0xFFFD] = 0x26
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x48)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CMP_IM_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 130
    mem.Data[0xFFFC] = cpu.INS_CMP_IM
    mem.Data[0xFFFD] = 0x26
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 130)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CMP_IM_Neg2():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 8
    mem.Data[0xFFFC] = cpu.INS_CMP_IM
    mem.Data[0xFFFD] = 0x26
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 8)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CMP_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_ZP
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 3)

@runTest()
def TEST_CMP_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_ZPX
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CMP_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_ABS
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CMP_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_ABSX
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CMP_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_ABSY
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CMP_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_INDX
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x30
    mem.Data[0x0030] = 0x42
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_CMP_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0x42
    mem.Data[0xFFFC] = cpu.INS_CMP_INDY
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x30
    mem.Data[0x0030] = 0x42
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 5)


# CPX, CPY


@runTest()
def TEST_CPX_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPX_IM
    mem.Data[0xFFFD] = 0x42
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.X, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CPX_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPX_ABS
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.X, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CPX_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPX_ZP
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.X, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 3)

@runTest()
def TEST_CPY_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Y = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPY_IM
    mem.Data[0xFFFD] = 0x42
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.Y, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_CPY_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Y = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPY_ABS
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.Y, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_CPY_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.Y = 0x42
    mem.Data[0xFFFC] = cpu.INS_CPY_ZP
    mem.Data[0xFFFD] = 0x20
    mem.Data[0x0020] = 0x42
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.Y, 0x42)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 3)


# SBC


@runTest()
def TEST_SBC_IM():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = 0x0
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x0)
    expect_eq(cpu.Z, 1)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = 0x1
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -0x1)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_Neg_wCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 0
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = 0x1
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -0x2)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_Overflow():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    cpu.A = 127
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = -1
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 128)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.V, 1)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_NegCarry():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 0
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -0x1)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_Normal():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    cpu.A = 20
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = 17
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0x3)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_IM_NegNeg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = -20
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_SBC_IM
    mem.Data[0xFFFD] = -17
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -3)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.C, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_SBC_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_SBC_ABS
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0042] = 1
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, -1)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_SBC_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0
    cpu.C = 1
    mem.Data[0xFF00] = cpu.INS_SBC_ZP
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0042] = 0
    CyclesUsed = cpu.Execute(3, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 3)

@runTest()
def TEST_SBC_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0
    cpu.C = 1
    cpu.X = 5
    mem.Data[0xFF00] = cpu.INS_SBC_ZPX
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 0
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_SBC_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0
    cpu.C = 1
    cpu.X = 5
    mem.Data[0xFF00] = cpu.INS_SBC_ABSX
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 0
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_SBC_ABSY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem, vector=0xFF00)
    cpu.A = 0
    cpu.C = 1
    cpu.Y = 5
    mem.Data[0xFF00] = cpu.INS_SBC_ABSY
    mem.Data[0xFF01] = 0x42
    mem.Data[0x0047] = 0
    CyclesUsed = cpu.Execute(4, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 4)

@runTest()
def TEST_SBC_INDX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 0x04
    cpu.A = 0
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_SBC_INDX
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0006] = 0x00
    mem.Data[0x0007] = 0x80
    mem.Data[0x8000] = 0
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_SBC_INDY():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0
    cpu.Y = 0x04
    mem.Data[0xFFFC] = cpu.INS_ADC_INDY
    mem.Data[0xFFFD] = 0x02
    mem.Data[0x0002] = 0x00
    mem.Data[0x0003] = 0x80
    mem.Data[0x8004] = 0
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.V, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 5)


# ASL


@runTest()
def TEST_ASL_AC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 1
    mem.Data[0xFFFC] = cpu.INS_ASL_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 2)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ASL_AC_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 0b11000000
    mem.Data[0xFFFC] = cpu.INS_ASL_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0b10000000)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ASL_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ASL_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 1
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x0042], 2)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.N, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 5)

@runTest()
def TEST_ASL_ZP_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ASL_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0b11000000
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x0042], 0b10000000)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 5)

@runTest()
def TEST_ASL_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ASL_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0b11000000
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0042], 0b10000000)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ASL_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ASL_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0b11000000
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0042], 0b10000000)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.N, 1) 
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ASL_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ASL_ABSX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0b11000000
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(mem.Data[0x0042], 0b10000000)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.N, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 7)


# LSR


@runTest()
def TEST_LSR_AC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 1
    cpu.N = 1
    cpu.C = cpu.Z = 0
    mem.Data[0xFFFC] = cpu.INS_LSR_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_LSR_AC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 4
    mem.Data[0xFFFC] = cpu.INS_LSR_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 2)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_LSR_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_LSR_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 0
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x0042], 0)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 5)

@runTest()
def TEST_LSR_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 1
    mem.Data[0xFFFC] = cpu.INS_LSR_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0043] = 0
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0043], 0)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_LSR_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_LSR_ABS
    mem.Data[0xFFFD] = 0x43
    mem.Data[0x0043] = 0
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0043], 0)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_LSR_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 5
    mem.Data[0xFFFC] = cpu.INS_LSR_ABSX
    mem.Data[0xFFFD] = 0x43
    mem.Data[0x0048] = 9
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(mem.Data[0x0048], 4)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 7)


# ROL, ROR


@runTest()
def TEST_ROL_AC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 1
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROL_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 3)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ROL_AC_Zero():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 128
    mem.Data[0xFFFC] = cpu.INS_ROL_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ROL_AC_Neg():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.A = 64
    mem.Data[0xFFFC] = cpu.INS_ROL_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -128)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 1)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ROL_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROL_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 5
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x0042], 11)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 5)

@runTest()
def TEST_ROL_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROL_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 5
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0042], 11)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ROL_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROL_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 5
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0042], 11)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ROL_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROL_ABSX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 5
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(mem.Data[0x0042], 11)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(cpu.N, 0)
    expect_eq(CyclesUsed, 7)

@runTest()
def TEST_ROR_AC():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.C = 1
    mem.Data[0xFFFC] = cpu.INS_ROR_AC
    CyclesUsed = cpu.Execute(2, mem)
    expect_eq(cpu.A, -128)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 2)

@runTest()
def TEST_ROR_ZP():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ROR_ZP
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0042] = 1 
    CyclesUsed = cpu.Execute(5, mem)
    expect_eq(mem.Data[0x0042], 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 5)

@runTest()
def TEST_ROR_ZPX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 1
    mem.Data[0xFFFC] = cpu.INS_ROR_ZPX
    mem.Data[0xFFFD] = 0x42
    mem.Data[0x0043] = 1 
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x0043], 0)
    expect_eq(cpu.C, 1)
    expect_eq(cpu.Z, 1)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ROR_ABS():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_ROR_ABS
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x42
    mem.Data[0x4242] = 10
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(mem.Data[0x4242], 5)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 6)

@runTest()
def TEST_ROR_ABSX():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpu.X = 2
    mem.Data[0xFFFC] = cpu.INS_ROR_ABSX
    mem.Data[0xFFFD] = 0xFE
    mem.Data[0xFFFE] = 0x42
    mem.Data[0x4300] = 10
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(mem.Data[0x4300], 5)
    expect_eq(cpu.C, 0)
    expect_eq(cpu.Z, 0)
    expect_eq(CyclesUsed, 7)


# BRK, RTI


@runTest()
def TEST_BRK():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    mem.Data[0xFFFC] = cpu.INS_BRK
    mem.Data[0xFFFE] = 0x00
    mem.Data[0xFFFF] = 0x80
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(cpu.B, 1)
    expect_eq(cpu.PC, 0x8000)
    expect_eq(CyclesUsed, 7)
    expect_eq(mem.Data[(0x100 | cpuCopy.SP)+3], 0xFF)
    expect_eq(mem.Data[(0x100 | cpuCopy.SP)+2], 0xFC)
    expect_eq(mem.Data[(0x100 | cpuCopy.SP)+1], cpuCopy.PS)

@runTest()
def TEST_RTI():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    cpuCopy = cpu
    mem.Data[0xFFFC] = cpu.INS_BRK
    mem.Data[0xFFFE] = 0x00
    mem.Data[0xFFFF] = 0x80
    mem.Data[0x8000] = cpu.INS_RTI
    CyclesUsed = cpu.Execute(7, mem)
    expect_eq(CyclesUsed, 7)
    CyclesUsed = cpu.Execute(6, mem)
    expect_eq(CyclesUsed, 6)
    expect_eq(cpu.PC, 0xFFFD)
    expect_eq(cpuCopy.PS, cpu.PS)


# Programs


@runTest()
def TEST_PRG_INIT():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    Prg = [0x00,0x10,0xA9,0xFF,0x85,0x90,0x8D,0x00,0x80,0x49,0xCC,0x4C,0x02,0x10]
    cpu.LoadProgram(Prg, mem)
    expect_eq(mem.Data[0x0FFF], 0x00)
    expect_eq(mem.Data[0x1000], 0xA9)
    expect_eq(mem.Data[0x1001], 0xFF)
    expect_eq(mem.Data[0x1002], 0x85)
    ...
    expect_eq(mem.Data[0x1009], 0x4C)
    expect_eq(mem.Data[0x100A], 0x02)
    expect_eq(mem.Data[0x100B], 0x10)
    expect_eq(mem.Data[0x100C], 0x00)

@runTest()
def TEST_PRG_1():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    Prg = [0x00,0x10,0xA9,0xFF,0x85,0x90,0x8D,0x00,0x80,0x49,0xCC,0x4C,0x02,0x10]
    cpu.PC = cpu.LoadProgram(Prg, mem)
    Clock = 1000
    while Clock > 0:
        Clock -= cpu.Execute(20, mem)
    expect_eq(cpu.A, 255)

@runTest()
def TEST_PRG_2():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    Prg = [0x00,0x10,0xA9,0x00,0x85,0x42,0xE6,0x42,0xA6,0x42,0xE8,0x4C,0x04,0x10]
    cpu.PC = cpu.LoadProgram(Prg, mem)
    Clock = 1000
    while Clock > 0:
        Clock -= cpu.Execute(1, mem)

@runTest(-1)
def TEST_PRG_3():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    Prg = [0x00,0x10,0xA9,0x00,0x18,0x69,0x08,0xC9,0x18,0xD0,0xFA,0xA2,0x14]
    cpu.PC = cpu.LoadProgram(Prg, mem)
    Clock = 1000
    while Clock > 0:
        Clock -= cpu.Execute(1, mem)

@runTest(-1)
def TEST_PRG_3():
    import binascii
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    Prg = [0x0a, 0x00]
    path = '\\'.join(__file__.split('\\')[:-1]) + '\\6502_Tests2\\6502_functional_test.bin'
    with open(path, 'rb') as f:
        hexcode = binascii.hexlify(f.read())
    hexcode = str(hexcode).strip("b'").strip("'")
    for i in range(len(hexcode)//2):
        Prg.append(int('0x' + hexcode[i*2:i*2+2], 16))
    cpu.LoadProgram(Prg, mem)
    cpu.PC = 0x400
    while True:
        cpu.Execute(1, mem)


# Shows final results
showTestResults()
