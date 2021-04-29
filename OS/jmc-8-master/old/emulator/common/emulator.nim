import ../../common/jmc, ../../common/util

template emulatorAssert(condition: bool, message: string): void =
    if not condition:
        raise newException(Exception, "Emulator error: " & message)

# Loads a memory image into the JMCs memory
proc loadMemory*(self: JMCState, image: seq[uint8], location: uint): void =
    for i, b in image.pairs():
        self.memory[location + i.uint] = b

# Cycles the CPU once
proc executeNext*(self: JMCState): void =
    proc pcnext(): uint8 =
        result = self.memory[self.programCounter]
        self.programCounter += 1
        emulatorAssert(self.programCounter <= 0xFFFF, "PC overflow")

    let
        instructionWord = pcnext()
        instruction = Instruction((instructionWord shr 4) and 0xF)
        reg0 = Register(instructionWord and 0x7)
        constArgs = (instructionWord and 0x8) == 0

    case instruction
    of Instruction.PUSH:
        self.stackPointer -= 1
        self.memory[self.stackPointer] = if constArgs: pcnext() else: self.registers[reg0]
    of Instruction.POP:
        self.registers[reg0] = self.memory[self.stackPointer]
        self.stackPointer += 1
    of Instruction.JNZ:
        let v = if constArgs: pcnext() else: self.registers[reg0] 
        if v != 0:
            self.programCounter = self.indirectAddress
    of Instruction.MW:
        self.registers[reg0] = if constArgs: pcnext() else: self.registers[pcnext() and 0x7]
    of Instruction.LW, Instruction.SW:
        let address =
            if constArgs:
                pcnext().uint16 or (pcnext().uint16 shl 8)
            else:
                self.indirectAddress
        if instruction == Instruction.LW:
            self.registers[reg0] = self.memory[address]
        else:
            self.memory[address] = self.registers[reg0]
    of Instruction.LDA:
        self.registers[Register.J] = pcnext()
        self.registers[Register.I] = pcnext()
    of Instruction.ADD, Instruction.ADC, Instruction.SUB, Instruction.SBB,
        Instruction.AND, Instruction.OR, Instruction.NOR, Instruction.CMP:
        let
            arg0 = self.registers[reg0]
            arg1 = if constArgs: pcnext() else: self.registers[pcnext() and 0x7]
            value = case instruction
                    of Instruction.ADD: arg0 + arg1
                    of Instruction.ADC: arg0 + arg1 + self.flags.carry
                    of Instruction.SUB: arg0 - arg1
                    of Instruction.SBB: arg0 - arg1 - self.flags.borrow
                    of Instruction.AND: arg0 and arg1
                    of Instruction.OR: arg0 or arg1
                    of Instruction.NOR: not (arg0 or arg1)
                    of Instruction.CMP: 0
                    else: 0

        # Set flags
        if instruction == Instruction.CMP:
            self.flags.less = arg0 < arg1
            self.flags.equal = arg0 == arg1
            self.flags.greater = arg0 > arg1
        elif instruction in { Instruction.ADD, Instruction.ADC, Instruction.SUB, Instruction.SBB }:
            let
                msb0 = bool((arg0 shr 7) and 1)
                msb1 = bool((arg1 shr 7) and 1)
                msbv = bool((value shr 7) and 1)

            self.flags.carry = (arg0.int + arg1.int) > 255
            self.flags.overflow =
                (msb0 and msb1 and not msbv) or ((not msb0) and (not msb1) and msbv)
            self.flags.borrow = (arg0.int - arg1.int) < 0

        # Set value
        if instruction != Instruction.CMP:
            self.registers[reg0] = value

proc executeCount*(self: JMCState, count: int): void =
    for i in 0..count-1:
        self.executeNext()