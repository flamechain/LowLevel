import unittest, os, strutils, sequtils
import ../../common/jmc
import emulator

const ASSEMBLER_PATH = "..\\assembler\\jmcasm.exe"

var
    state: JMCState

# Assembles a string of code and puts it into a location in the JMC state's memory
proc loadIntoState(code: string, location: uint): void =
    assert existsFile(ASSEMBLER_PATH)
    writeFile("temp.asm", code)

    # Execute the assembler
    discard execShellCmd("$1 $2 --out:$3" % [ASSEMBLER_PATH, "temp.asm", "temp.bin"])

    # Load assembled code into memory
    let codeString = readFile("temp.bin")
    var codeBytes = newSeq[uint8](codeString.len)
    for i, c in codeString.pairs():
        codeBytes[i] = c.uint8
    state.loadMemory(codeBytes, location)

    # Cleanup
    removeFile("temp.asm")
    removeFile("temp.bin")

# Declares a test for an arithmetic operation
template declArithmeticTest(instruction: string, op: untyped): untyped =
    test "" & instruction:
        loadIntoState("$1 a, 3\n$1 b, a" % [instruction], 0)
        state.registers[Register.A] = 0x55
        state.registers[Register.B] = 0x66

        state.executeCount(2)
        check(state.registers[Register.A] == op(0x55, 3))
        check(state.registers[Register.B] == op(0x66.uint8, state.registers[Register.A]))

suite "JMC-8 Emulator Unit Tests":
    # Create a new JMC state for each successive test
    setup:
        state = JMCState.new()

    test "Memory":
        for i in 0..65535:
            state.memory[i] = i mod 255

        for i in 0..65535:
            check(state.memory[i] == uint8(i mod 255))

    test "PUSH":
        loadIntoState("push 0x55", 0)
        state.stackPointer = 0x80FF
        state.executeNext()
        check(state.memory[state.stackPointer] == 0x55)
        check(state.stackPointer == 0x80FE)

    test "POP":
        loadIntoState("pop a", 0)
        
        # Simulate pushing a value onto the stack
        state.stackPointer = 0x80FF
        state.stackPointer -= 1
        state.memory[state.stackPointer] = 0x55

        state.executeNext()
        check(state.registers[Register.A] == 0x55)
        check(state.stackPointer == 0x80FF)

    test "JNZ":
        loadIntoState("lda [0x8000]\njnz 1", 0)
        state.executeCount(2)

        loadIntoState("lda [0xFFFF]\njnz 0", 0)
        state.programCounter = 0
        state.executeCount(2)
        check(state.programCounter == 5) # 5 is the number of bytes the above instructions take

        loadIntoState("lda [0x8000]\njnz a", 0)
        state.programCounter = 0
        state.registers[Register.A] = 0x02
        state.executeCount(2)
        check(state.programCounter == 0x8000)

    test "MW":
        loadIntoState("mw a, 1\nmw c, a", 0)
        state.executeCount(2)
        check(state.registers[Register.A] == 1)
        check(state.registers[Register.C] == 1)

    test "LW":
        loadIntoState("lw a, [0x8000]\nlda [0x8001]\nlw c", 0)
        state.memory[0x8000] = 0x55
        state.memory[0x8001] = 0x66

        state.executeCount(3)
        check(state.registers[Register.A] == 0x55)
        check(state.registers[Register.C] == 0x66)

    test "SW":
        loadIntoState("sw [0x8000], a\n lda [0x8001]\nsw a", 0)
        state.registers[Register.A] = 0x55
        state.executeCount(3)
        check(state.memory[0x8000] == 0x55)
        check(state.memory[0x8001] == 0x55)

    test "LDA":
        loadIntoState("lda [0x8000]\nlda [0x1234]\nlda [0x0000]", 0)
        
        state.executeCount(1)
        check(state.indirectAddress == 0x8000)

        state.executeCount(1)
        check(state.indirectAddress == 0x1234)

        state.executeCount(1)
        check(state.indirectAddress == 0x0000)

    declArithmeticTest("ADD", `+`)
    declArithmeticTest("ADC", proc(x, y: uint8): uint8 = x + y + state.flags.carry)
    declArithmeticTest("SUB", `-`)
    declArithmeticTest("SBB", proc(x, y: uint8): uint8 = x - y - state.flags.borrow)
    declArithmeticTest("AND", `and`)
    declArithmeticTest("OR", `or`)
    declArithmeticTest("NOR", proc(x, y: uint8): uint8 = not (x or y))

    test "CMP":
        loadIntoState("cmp a, b\ncmp a, 0xFF\ncmp a, 1", 0)
        state.registers[Register.A] = 1
        state.registers[Register.B] = 0

        state.executeCount(1)
        check(not state.flags.less)
        check(not state.flags.equal)
        check(state.flags.greater)

        state.executeCount(1)
        check(state.flags.less)
        check(not state.flags.equal)
        check(not state.flags.greater)

        state.executeCount(1)
        check(not state.flags.less)
        check(state.flags.equal)
        check(not state.flags.greater)

    test "Flags":
        loadIntoState("add a, 0xFF\nadd a, 127\nsub a, 1", 0)

        state.registers[Register.A] = 1
        state.executeCount(1)
        check(state.flags.carry)

        state.registers[Register.A] = 127
        state.executeCount(1)
        check(state.flags.overflow)

        state.registers[Register.A] = 0
        state.executeCount(1)
        check(state.flags.borrow)