# EMP32 Manual

## EMP32-1000 Instruction Encoding

| Opcode | Mode | Reg/Disp Size | Reg/Disp/Im Size | Reg/Disp/Im | Reg/Disp/Im |
|-|-|-|-|-|-|
| 8 | 4 | 2 | 2 | 8-32 | 8-32 |
|

- The first byte is the opcode
- The next 4 bits are the Mode<sup>2</sup>:
  - 0: Reg
  - 1: Im
  - 2: Disp
  - 3: RegDisp
  - 4: RegReg
  - 5: RegIm
  - 6: DispReg
  - 7: DispIm
  - 8: DispDisp
- The next 2 bits are the size for either a register<sup>1</sup> or a displacement<sup>2</sup>
- The next 2 bits are the size for either a register, displacement, or an immediate constant<sup>2</sup>
- The next 1-4 bytes are a register code (1 byte), displacement (1-4 bytes), or an immediate constant (1-4 bytes), where the byte size is chosen based on the correlating 2 bits defining the size
- The next 1-4 bytes are the same as the previous if the instruction requires 2 operands

___

<sup>1: Register codes are always 1 byte, so instead it decides what size of register to change e.g. al, ax, eax</sup>

<sup>2: With extra bits to spare for future expansion of either 64-bit mode, additional addressing modes, or new registers</sup>
