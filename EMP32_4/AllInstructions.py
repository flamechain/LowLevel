# Notes
bits = 32
full = 16**8
ram = range(65536, full)

### Modes
Addr_RegReg = 0x00
Addr_Reg = 0x01
Addr_RegDisp32 = 0x02
Addr_RegDisp16 = 0x03
Addr_RegDisp8 = 0x04
Addr_RegIm32 = 0x05
Addr_RegIm16 = 0x06
Addr_RegIm8 = 0x07
Addr_Disp32Im32 = 0x08
Addr_Disp16Im16 = 0x09
Addr_Disp8Im8 = 0x0A
Addr_Disp32Disp32 = 0x0B
Addr_Disp16Disp16 = 0x0C
Addr_Disp8Disp8 = 0x0D
Addr_Disp32 = 0x0E
Addr_Disp16 = 0x0F
Addr_Disp8 = 0x10
Addr_Im32Im32 = 0x11
Addr_Im16Im16 = 0x12
Addr_Im8Im8 = 0x13
Addr_Im32 = 0x14
Addr_Im16 = 0x15
Addr_Im8 = 0x16

### Register Codes
Code_EAX = 0x0
Code_EBX = 0x1
Code_ECX = 0x2
Code_EDX = 0x3
Code_ESI = 0x4
Code_EDI = 0x5
Code_ESP = 0x6
Code_EBP = 0x7
Code_AX = 0x8
Code_BX = 0x9
Code_CX = 0xA
Code_DX = 0xB
Code_BAX = 0xC
Code_BBX = 0xD
Code_BCX = 0xE
Code_BDX = 0xF

### General

# Holes: 0x18,

INT     = 0x00 # Interupt
HLT     = 0x01 # Halt
NOP     = 0x02 # No operation
CALL    = 0x03 # Call procedure
RET     = 0x42 # Return from procedure
LOCK    = 0x57 # Lock data bus for multicore
BUSY    = 0x5D # Set busy flag
IDLE    = 0x5E # Clear busy flag
WAIT    = 0x5F # Wait until busy flag clear
IN      = 0x60 # Input from port
OUT     = 0x61 # Output to port

### Arithmatic

# Basic
ADC     = 0x04 # Add with carry
ADD     = 0x05 # Add
IADD    = 0x06 # Signed add
FADD    = 0x07 # Float add

SBC     = 0x08 # Sub with carry
SUB     = 0x09 # Sub
ISUB    = 0x0A # Signed sub
FSUB    = 0x0B # Float sub

MLC     = 0x0C # Mul with carry
MUL     = 0x0D # Mul
IMUL    = 0x0E # Signed mul
FMUL    = 0x0F # Float mul

DVC     = 0x10 # Div with carry
DIV     = 0x11 # Div
IDIV    = 0x12 # Signed div
FDIV    = 0x13 # Float div

# Special
ABS     = 0x14 # Absolute value
FABS    = 0x15 # Float abs
CHS     = 0x16 # Change sign
FCHS    = 0x17 # Float chs

FINT    = 0x19 # Round to int

SCALE   = 0x1A # Slow scale
FSCALE  = 0x1B # Float scale
SQRT    = 0x1C # Square root
FSQRT   = 0x1D # Float dqrt

COS     = 0x1E # Cosine
SIN     = 0x1F # Sine
TAN     = 0x20 # tangant

FLD1    = 0x21 # Float load +1.0
FLDZ    = 0x22 # Float load +0.0
FLDPI   = 0x23 # Float load pi

INC     = 0x45 # Increment
DEC     = 0x46 # Decrement

# Bitwise
OR      = 0x24 # OR
AND     = 0x25 # AND
NOT     = 0x26 # NOT
XOR     = 0x27 # XOR

TST     = 0x28 # Test against 0
FTST    = 0x29 # Float tst

ROL     = 0x3C # Rotate left
ROR     = 0x3D # Rotate right
SHL     = 0x3E # Shift left
SHR     = 0x3F # Shift right
SAL     = 0x40 # Signed shl
SAR     = 0x41 # Signed shr

### Jump and Compare

CMP     = 0x2A # Compare
FCMP    = 0x2B # Float compare

JMP     = 0x2C # Jump
JMPAHD  = 0x63 # Jmp n places ahead
LOOP    = 0x43 # Loop with ecx as i

# Jump on flags
JO      = 0x2D # Jmp if overflow
JNO     = 0x2F # Jmp if not overflow
JS      = 0x30 # Jmp if sign
JNS     = 0x31 # Jmp if not sign
JC      = 0x32 # Jmp in carry
JNC     = 0x33 # Jmp if not carry
JZ      = 0x34 # Jmp if zero
JNZ     = 0x35 # Jmp if not zero

# Jump on value
JE      = 0x36 # Jmp if equal
JNE     = 0x37 # Jmp if not equal
JG      = 0x38 # Jmp if greater
JGE     = 0x39 # Jmp if greater or equal
JL      = 0x3A # Jmp if less
JLE     = 0x3B # Jmp if less or equal

### Transfers

MOV     = 0x44 # Move [a]|a, [b]|b
XCHG    = 0x58 # Exchange bytes
XCHGW   = 0x59 # Exchange words
XCHGE   = 0x5A # Exchange effective address
BSWAP   = 0x5B # Byte swap, for little -> big
EFLIP   = 0x5C # Flip effective address, little -> big
LDAO    = 0x62 # Load address offset
STAO    = 0x63 # Store address offset

# Flags
CLC     = 0x47 # Clear carry
STC     = 0x48 # Set carry
CLO     = 0x49 # Clear overflow
STO     = 0x4A # Set overflow
CLZ     = 0x4B # Clear zero
STZ     = 0x4C # Set zero
CLS     = 0x4D # Clear sign
STS     = 0x4E # Set sign
CLI     = 0x4F # Clear interupt
STI     = 0x50 # Set interupt

# Stack
POP     = 0x51 # Pop byte
POPE    = 0x52 # Pop effective address
POPF    = 0x53 # Pop flags
PUSH    = 0x54 # Push byte
PUSHE   = 0x55 # Push effective address
PUSHF   = 0x56 # Push flags

# Reserved Codes
Reserved = [
    0xCC # Breakpoint
]
