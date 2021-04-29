# JMC-8 Documentation

TODO: Insert a description here

#### Notes

- Little endian
- PC is mapped to 0xFFFC
- SP is mapped to 0xFFFE

#### Instruction layout

All instructions are in the `XXXXYZZZ` format.

- X represents 4-bit instruction identifier
- Y is 1 if the instruction arguments are in registers, 0 if they are constants
  - Y value of 0 on a single-argument instruction (`PUSH` or `MW`) means that the argument is an 8-bit constant in the next word
- Z represents the register identifier of the first register argument

Instructions can be followed by 0-2 argument bytes depending on the instruction.  If it is an instruction with a single register argument (i.e. `PUSH`/`POP`) then it is followed by 0 bytes. If it is an instruction with a memory addess argument (`LW`/`SW`) and the instruction's Y-bit is zero then it is proceeded by 2 bytes denoting the memory address target of the instruction (little endian).

For a `LW` or `SW` instruction where the Y-bit is 1, the destination of `LW` and the source of `SW` are stored within the first instruction byte. The memory address of the instruction is assumed to be `[IJ]`

#### Instructions

```assembly
(0x07) ADD* reg, imm/reg            -> reg = arg0 + arg1
(0x08) ADC* reg, imm/reg            -> reg = arg0 + arg1 + c
(0x09) SUB* reg, imm/reg            -> reg = arg0 - arg1
(0x0A) SBB* reg, imm/reg            -> reg = arg0 - arg1 - b
(0x0B) AND  reg, imm/reg            -> reg = arg0 & arg1
(0x0C) OR   reg, imm/reg            -> reg = arg0 | arg1
(0x0D) NOR  reg, imm/reg            -> reg = ~(arg0 | arg1)
(0x0E) CMP  reg, imm/reg            -> Compare args, load F 
(0x00) PUSH imm/reg                 -> [--SP] = arg0
(0x01) POP  reg                     -> arg0 = [SP++]
(0x02) JNZ  imm/reg                 -> imm/reg > 0 ? PC = IJ
(0x03) MW   reg, imm/reg            -> arg0 = arg1
(0x04) LW   reg, [IJ]/[imm]         -> arg0 = [arg1]
(0x05) SW   [IJ]/[imm], reg         -> [arg0] = arg1
(0x06) LDA  [imm]                   -> IJ = imm
```

*ADD, ADC, SUB, and SBB will load the carry or borrow bits in the F register*

#### Registers

```assembly
A (0x00) - General purpose register
B (0x01) - General purpose register
C (0x02) - General purpose register
D (0x03) - General purpose register
I (0x04) - Index high byte/general purpose register
J (0x05) - Index low byte/general purpose register
Z (0x06) - Subroutine return value/general purpose register
F (0x07) - Flags register
    Layout of F (low bit to high bit):
    Less than (<)
    Equal to (=)
    Greater than (>)
    Carry (C)
    Borrow (B)
    Overflow (O)
```

#### Macros

To make up for missing functionality, the JMC-8 assembler has built-in macros that expand out to other instructions in order to improve functionality and programmability. These are written in the assembler's macro syntax.

NOTE: Some macros will trash the F register. Macros that specifically deal with memory might trash the I and J registers.

```assembly
# LW override that automatically loads I and J
LW %r0, [%i1]:
    lda %i1
    lw %r0

# Override for register memory address  
LW %r0, [%r1, %r2]:
    mw i, %r1
    mw j, %r2
    lw %r0
    
# SW override that automatically loads I and J
SW [%i0], %r1:
    lda %i0
    sw %r1
    
# Override for register memory address
SW [%r0, %r1], %r2:
    mw i, %r0
    mw j, %r1
    sw %r2

# Call a subroutine at a known location
CALL [%i0]:
    push $.high
    push $.low
    lda %i0
    jnz 1
    
# Call a subroutine at an unknown location
CALL [%r0, %r1]:
    push $.high
    push $.low
    mw i, %r0
    mw j, %r1
    jnz 1

# Return from a subroutine
RET:
    pop i
    pop j
    jnz 1

# Jump if less than
JLT %r0, %x1:
    cmp %r0, %x1
    and f, 0x01
    jnz f

# Jump if less than or equal to
JLT %r0, %x1:
    cmp %r0, %x1
    and f, 0x03
    jnz f

# Jump if equal to
JEQ %r0, %x1:
    cmp %r0, %x1
    and f, 0x02
    jnz f

# Jump if greater than
JGT %r0, %x1:
    cmp %r0, %x1
    and f, 0x04
    jnz f

# Jump if greater than or equal to
JGT %r0, %x1:
    cmp %r0, %x1
    and f, 0x06
    jnz f

# Jump if zero
JZ %r0:
    jeq %r0, f
    
# Jump if carry
JC:
    and f, 0x08
    jnz f
    
# Jump if borrow
JB:
    and f, 0x10
    jnz f

# Jump if overflow
JO:
    and f, 0x20
    jnz f
    
# Bitwise NOT
NOT %r0:
    nor %r0, %r0

# Bitwise NAND
NAND %r0, %x1:
    and %r0, %x1
    not %r0

# Bitwise XNOR
XNOR %r0, %x1:
    mw f, %x1
    nand f, %r0
    or %r0, %x1
    and %r0, f

# Bitwise XOR
XOR %r0, %x1:
    mw f, %x1
    or f, %r0
    nand %r0, %x1
    and %r0, f
```