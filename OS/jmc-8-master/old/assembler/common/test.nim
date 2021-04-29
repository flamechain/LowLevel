import unittest, os, strutils, sequtils
import ../../common/jmc
import assembler

const integerTestingConstants = [0x00, 0x01, 0x55, 0xFE, 0xFF]
const addressTestingConstants = [0x0000, 0x0001, 0x00FF, 0x10FF, 0x8000, 0x5555, 0xFFFE, 0xFFFF]

proc checkASM(code: string, expected: seq[int]): void =
    let assembled = assemble("no_file", code).mapIt(it.int)
    check(assembled == expected)

template declArithmeticTest(instruction: string): untyped =
    test "" & instruction:
        let opcode = parseEnum[Instruction](instruction).int

        for r in Register.A..Register.F:
            for c in integerTestingConstants:
                checkASM(instruction & " " & $r & ", " & $c, @[(opcode shl 4) or r.int, c])

            for rb in Register.A..Register.F:
                checkASM(instruction & " " & $r & ", " & $rb, @[(opcode shl 4) or 0x08 or r.int, rb.int])

template declRegisterAndConstantTest(instruction: string): untyped =
    test "" & instruction:
        let opcode = parseEnum[Instruction](instruction).int

        for c in integerTestingConstants:
            checkASM(instruction & " " & $c, @[opcode shl 4, c])

        for r in Register.A..Register.F:
            checkASM(instruction & " " & $r, @[(opcode shl 4) or 0x08 or r.int])

template declRegisterTest(instruction: string): untyped =
    test "" & instruction:
        let opcode = parseEnum[Instruction](instruction).int

        for r in Register.A..Register.F:
            checkASM(instruction & " " & $r, @[(opcode shl 4) or 0x08 or r.int])

suite "JMC-8 Assembler Unit Tests":
    setup:
        discard

    declArithmeticTest("ADD")
    declArithmeticTest("ADC")
    declArithmeticTest("SUB")
    declArithmeticTest("SBB")
    declArithmeticTest("AND")
    declArithmeticTest("OR")
    declArithmeticTest("NOR")
    declArithmeticTest("CMP")
    declArithmeticTest("MW")
    
    declRegisterTest("POP")

    declRegisterAndConstantTest("PUSH")
    declRegisterAndConstantTest("JNZ")

    test "LW":
        for r in Register.A..Register.F:
            checkASM("LW " & $r, @[(Instruction.LW.int shl 4) or 0x08 or r.int])

            for c in addressTestingConstants:
                checkASM(
                    "LW " & $r & ", [" & $c & "]", @[(Instruction.LW.int shl 4) or r.int,
                    c and 0xFF, (c shr 8) and 0xFF]
                )

    test "SW":
        for r in Register.A..Register.F:
            checkASM("SW " & $r, @[(Instruction.SW.int shl 4) or 0x08 or r.int])

            for c in addressTestingConstants:
                checkASM(
                    "SW [" & $c & "], " & $r, @[(Instruction.SW.int shl 4) or r.int,
                    c and 0xFF, (c shr 8) and 0xFF]
                )

    test "LDA":
        for c in addressTestingConstants:
            checkASM(
                "LDA [" & $c & "]", @[(Instruction.LDA.int shl 4),
                c and 0xFF, (c shr 8) and 0xFF]
            )