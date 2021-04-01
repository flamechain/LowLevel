# RBIF (Reduced Bit Instruction Format)

## V1

| Size | Mode | Opcode | Operand 1 | Operand 2 |
|-|-|-|-|-|
| 4 | 4 | 8 | 0-64 | 0-64 |
|

## V2

Sizes: S, 16, 32, 64
Modes: DispReg, RegDisp, RegIm, DispIm

Only need 2 bits for Size, and 2 bits for modes. Only leaves 16 instructions left.

## V3

Sizes: 8, 16, 32, 64
Modes: Disp, Reg, Im, RegDisp, RegReg, RegIm, DispIm, DispReg

Mode Byte

| Size | Mode | 
