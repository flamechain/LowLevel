# Instructions Full Reference

## Contents

- [1.0 Quick Reference](#10-quick-reference)
- [2.0 Reference](#20-reference)
- [3.0 Full Reference](#30-full-reference)

## 1.0 Quick Reference

| Mnemonic | Summary | Opcode |
|-|-|-|
| [ABS](#abs) | Absolute value | $14 |
| [ADC](#adc) | Unsigned addition with carry | $04 |
| [ADD](#add) | Unsigned addition | $05 |
| [AND](#and) | Bitwise AND | $25 |
| [BSWAP](#bswap) | Swaps adjacent bytes | $5B |
| [BUSY](#busy) | Sets busy flag | $5D |
| [CALL](#call) | Jump to subroutine | $03 |
| [CHS](#chs) | Change sign | $16 |
| [CLC](#clc) | Clear carry flag | $47 |
| [CLI](#cli) | Clear interupt disable flag | $4F |
| [CLO](#clo) | Clear overflow flag | $49 |
| [CLS](#cls) | Clear sign flag | $4D |
| [CLZ](#clz) | Clear zero flag | $4B |
| [CMP](#cmp) | Compare two operands | $2A |
| [COS](#cos) | Cosine | $1E |
| [DEC](#dec) | Decrement by 1 | $46 |
| [DIV](#div) | Unsigned divide | $11 |
| [DVC](#dvc) | Unsigned divide with carry | $10 |
| [EFLIP](#eflip) | Flip effective address | $5C |
| [FABS](#fabs) | Double-precision absolute value | $15 |
| [FADD](#fadd) | Double-precision signed addition | $07 |
| [FCHS](#fchs) | Double-precision change sign | $17 |
| [FCMP](#fcmp) | Compare two double-precision operands | $2B |
| [FDIV](#fdiv) | Double-precision signed division | $13 |
| [FINT](#fint) | Round to integer | $19 |
| [FLD1](#fld1) | Load double-precision +1.0 | $21 |
| [FLDPI](#fldpi) | Load double-precision pi | $23 |
| [FLDZ](#fldz) | Load double-precision +0.0 | $22 |
| [FMUL](#fmul) | Double-precision signed multiplication | $0F |
| [FSCALE](#fscale) | Fast double-precision scale | $1B |
| [FSQRT](#fsqrt) | Square-root | $1D |
| [FSUB](#fsub) | Double-precision signed subtraction | $0B |
| [FTST](#ftst) | Compare double-precision operand agaist zero | $29 |
| [HLT](#hlt) | Halt | $01 |
| [IADD](#iadd) | Signed addition | $06 |
| [IDLE](#idle) | Clear busy flag | $5E |
| [IDIV](#idiv) | Signed division | $12 |
| [IMUL](#imul) | Signed multiplication | $0E |
| [IN](#in) | Input from port | $60 |
| [INC](#inc) | Increment by 1 | $45 |
| [INT](#int) | Invoke interupt | $00 |
| [ISUB](#isub) | Signed subtraction | $0A |
| [JC](#jc) | Jump if carry flag set | $32 |
| [JE](#je) | Jump if equal | $36 |
| [JG](#jg) | Jump if greater than | $38 |
| [JGE](#jge) | Jump if greater than or equal to | $39 |
| [JL](#jl) | Jump if less than | $3A |
| [JLE](#jle) | Jump if less than or equal to | $3B |
| [JMP](#jmp) | Jump | $2C |
| [JMPAHD](#jmpahd) | Jump ahead | $63 |
| [JNC](#jnc) | Jump if carry flag clear | $33 |
| [JNE](#jne) | Jump if not equal | $37 |
| [JNO](#jno) | Jump if overflow flag clear | $2F |
| [JNS](#jns) | Jump is sign flag clear | $31 |
| [JNZ](#jnz) | Jump if zero flag clear | $35 |
| [JO](#jo) | Jump if overflow flag set | $2D |
| [JS](#js) | Jump if sign flag set | $30 |
| [JZ](#jz) | Jump if zero flag set | $34 |
| [LDAO](#ldao) | Load into EAO registers | $62 |
| [LOCK](#lock) | Lock data bus | $57 |
| [LOOP](#loop) | Loop | $43 |
| [MLC](#mlc) | Unsigned multiplication with carry | $0C |
| [MOV](#mov) | Move | $44 |
| [MUL](#mul) | Unsigned multiplication | $0D |
| [NOT](#not) | Bitwise NOT | $26 |
| [NOP](#nop) | No operation | $02 |
| [OUT](#out) | Output to port | $61 |
| [OR](#or) | Bitwise OR | $24 |
| [POP](#pop) | Pop byte from stack | $51  |
| [POPE](#pope) | Pop effective address from stack | $52 |
| [POPF](#popf) | Pop byte into flags register | $53 |
| [PUSH](#push) | Push byte onto stack | $54 |
| [PUSHE](#pushe) | Push effective address onto stack | $55 |
| [PUSHF](#pushf) | Push flags register onto stack | $56 |
| [RET](#ret) | Return from subroutine | $42 |
| [ROL](#rol) | Rotate left | $3C |
| [ROR](#ror) | Rotate right | $3D |
| [SAL](#sal) | Signed shift left | $40 |
| [SAR](#sar) | Signed shift right | $41 |
| [SBC](#sbc) | Unsigned subtraction with carry | $08 |
| [SCALE](#scale) | Integral scale | $1A |
| [SHL](#shl) | Shift left | $3E |
| [SHR](#shr) | Shift right | $3F |
| [SIN](#sin) | Sine | $1F |
| [SQRT](#sqrt) | Rounded square-root | $1D |
| [STAO](#stao) | Store EAO | $63 |
| [STC](#stc) | Set carry flag | $48 |
| [STI](#sti) | Set interupt disable flag | $50 |
| [STO](#sto) | Set overflow flag | $4A |
| [STS](#sts) | Set sign flag | $4E |
| [STZ](#stz) | Set zero flag | $4C |
| [SUB](#sub) | Unsigned subtraction | $09 |
| [TAN](#tan) | Tangent | $20 |
| [TST](#tst) | Compare operand agaist zero | $28 |
| [WAIT](#wait) | Halt until busy flag clear | $5F |
| [XCHG](#xchg) | Exchange bytes | $58 |
| [XCHGE](#xchge) | Exchange effective address | $5A |
| [XCHGW](#xchgw) | Exchange words | $59 |
| [XOR](#xor) | Bitwise XOR | $27 |
||

___

## 2.0 Reference

### 2.1 Data Transfers

| Mnemonic | Opcode |
|-|-|
| [MOV](#mov) | $44 |
| [XCHG](#xchg) | $58 |
| [XCHGW](#xchgw) | $59 |
| [XCHGE](#xchge) | $5A |
| [BSWAP](#bswap) | $5B |
| [EFLIP](#eflip) | $5C |
| [LDAO](#ldao) | $62 |
| [STAO](#stao) | $63 |
| [FLD1](#fld1) | $21 |
| [FLDZ](#fldz) | $22 |
| [FLDPI](#fldpi) | $23 |
||

### 2.2 Stack Operations

| Mnemonic | Opcode |
|-|-|
| [POP](#pop) | $51 |
| [POPE](#pope) | $52 |
| [POPF](#popf) | $53 |
| [PUSH](#push) | $54 |
| [PUSHE](#pushe) | $55 |
| [PUSHF](#pushf) | $56 |
||

### 2.3 Logical

| Mnemonic | Opcode |
|-|-|
| [OR](#or) | $24 |
| [AND](#and) | $25 |
| [NOT](#not) | $26 |
| [XOR](#xor) | $27 |
||

### 2.4 Arithmatic

| Mnemonic | Opcode |
|-|-|
| [ADC](#adc) | $04 |
| [ADD](#add) | $05 |
| [IADD](#iadd) | $06 |
| [FADD](#fadd) | $07 |
| [SBC](#sbc) | $08 |
| [SUB](#sub) | $09 |
| [ISUB](#isub) | $0A |
| [FSUB](#fsub) | $0B |
| [MLC](#mlc) | $0C |
| [MUL](#mul) | $0D |
| [IMUL](#imul) | $0E |
| [FMUL](#fmul) | $0F |
| [DVC](#dvc) | $10 |
| [DIV](#div) | $11 |
| [IDIV](#idiv) | $12 |
| [FDIV](#fdiv) | $13
| [ABS](#abs) | $14 |
| [FABS](#fabs) | $15 |
| [CHS](#chs) | $16 |
| [FCHS](#fchs) | $17 |
| [FINT](#fint) | $19 |
| [SCALE](#scale) | $1A |
| [FSCALE](#fscale) | $1B |
| [SQRT](#sqrt) | $1C |
| [FSQRT](#fsqrt) | $1D |
| [COS](#cos) | $1E |
| [SIN](#sin) | $1F |
| [TAN](#tan) | $20 |
| [INC](#inc) | $45 |
| [DEC](#dec) | $46 |
||

### 2.5 Shifts

| Mnemonic | Opcode |
|-|-|
| [ROL](#rol) | $3C |
| [ROR](#ror) | $3D |
| [SHL](#shl) | $3E |
| [SHR](#shr) | $3F |
| [SAL](#sal) | $40 |
| [SAR](#sar) | $41 |
||

### 2.6 Control of Flow & Compare

| Mnemonic | Opcode |
|-|-|
| [CMP](#cmp) | $2A |
| [FCMP](#fcmp) | $2B |
| [TST](#tst) | $28 |
| [FTST](#ftst) | $29 |
| [CALL](#call) | $03 |
| [RET](#ret) | $42 |
||
| [Jmp](#jmp) | $2C |
| [JMPAHD](#jmpahd) | $63 |
| [LOOP](#loop) | $43 |
| [JO](#jo) | $2D |
| [JNO](#jno) | $2F |
| [JS](#js) | $30 |
| [JNS](#jns) | $31 |
| [JC](#jc) | $32 |
| [JNC](#jnc) | $33 |
| [JZ](#jz) | $34 |
| [JNZ](#jnz) | $35 |
| [JE](#je) | $36 |
| [JNE](#jne) | $37 |
| [JG](#jg) | $38 |
| [JGE](#jge) | $39 |
| [JL](#jl) | $3A |
| [JLE](#jle) | $3B |
||

### 2.7 Flag Changes

| Mnemonic | Opcode |
|-|-|
| [CLC](#clc) | $47 |
| [STC](#stc) | $48 |
| [CLO](#clo) | $49 |
| [STO](#sto) | $4A |
| [CLZ](#clz) | $4B |
| [STZ](#stz) | $4C |
| [CLS](#cls) | $4D |
| [STS](#sts) | $4E |
| [CLI](#cli) | $4F |
| [STI](#sti) | $50 |
| [BUSY](#busy) | $5D |
| [IDLE](#idle) | $5E |
||

### 2.8 System Functions

| Mnemonic | Opcode |
|-|-|
| [INT](#int) | $00 |
| [HLT](#hlt) | $01 |
| [NOP](#nop) | $02 |
| [LOCK](#lock) | $57 |
| [WAIT](#wait) | $5F |
| [IN](#in) | $60 |
| [OUT](#out) | $61 |
||

___

## 3.0 Full Reference

All of the EMP32 instructions are here with full descriptions.

## ABS

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 14 | ABS | Rd | N/A |

### Description

Converts signed integer (Rd) positive if sign bit is set

### Affected Flags

- Clears sign flag

## ADC

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 04 | ADC | Rd | Rs |

### Description

Add the source and destination together with the carry, and store the result back into the destination.

### Affected Flags

- Sets sign flag if result was negative
- Sets zero flag if result was zero
- Sets carry flag if carry
- Sets overflow flag if the carry<sub>in</sub> and carry<sub>out</sub> xor to 1

## ADD

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 05 | ADD | Rd | Rs |

### Description

Add the source and destination together, and store the result back into the destination.

### Affected Flags

- Sets sign flag if result was negative
- Sets zero flag if result was zero
- Sets carry flag if carry

## AND

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 25 | AND | Rd | Rs |

### Description

Bitwise AND the source and destination, and store the result back into the destination.

### Affected Flags

- Sets zero flag if result was zero

## BSWAP

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 5B | BSWAP | Rd | N/A |

### Description

Takes 16-bit value (Rd) and swaps the bytes endianess.

### Affected Flags

- None

## BUSY

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 5D | BUSY | N/A | N/A |

### Description

Sets busy flag

### Affected Flags

- Sets busy flag

## CALL

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 03 | CALL | Rm | N/A |

### Description

Pushes program counter onto stack, then jumps to Rm.

### Affected Flags

- None

## CHS

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 16 | CHS | Rd | N/A |

### Description

Changes sign of signed integer, regardless if its already positive or negative. Stores result back into Rd.

### Affected Flags

- Sets sign flag if result is negative

## CLC

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 47 | CLC | N/A | N/A |

### Description

Clears carry flag

### Affected Flags

- Clears carry flag

## CLI

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 4F | CLI | N/A | N/A |

### Description

Clears interupt disable flag

### Affected Flags

- Clears interupt disable flag

## CLO

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 49 | CLO | N/A | N/A |

### Description

Clears overflow flag

### Affected Flags

- Clears overflow flag

## CLS

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 4D | CLS | N/A | N/A |

### Description

Clears sign flag

### Affected Flags

- Clears sign flag

## CLZ

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 4B | CLZ | N/A | N/A |

### Description

Clears zero flag

### Affected Flags

- Clears zero flag

## CMP

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 2A | CMP | Rm | Rn |

### Description

Subtracts Rm from Rn, and sets flags accordingly. Does not store result.

### Affected Flags

- Sets zero flag if result is zero
- Sets sign flag if results is negative

## COS

| Opcode | Instruction | Operand 1 | Operand 2 |
|-|-|-|-|
| 1E | COS | Rd | N/A |

### Description

Gets cosine of Rd, then stores result back into Rd as double-precision floating point.

### Affected Flags

- Sets zero flag if result is zero
- Sets sign flag if results is negative

___

<sub>[Top of File](#instructions-full-reference)</sub>
