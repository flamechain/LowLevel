# Instruction Prefixes (4-bits)
Pre_8    = 0x0 << 4
Pre_16   = 0x1 << 4
Pre_32   = 0x2 << 4
Pre_64   = 0x3 << 4
Pre_128  = 0x4 << 4
Pre_256  = 0x5 << 4
Pre_512  = 0x6 << 4
Pre_64F  = 0x7 << 4
Pre_80F  = 0x8 << 4
Pre_128F = 0x9 << 4

# Addressing Modes (4-bits)
Addr_Disp    = 0x0
Addr_Im      = 0x1
Addr_Reg     = 0x2
Addr_RegReg  = 0x3
Addr_RegDisp = 0x4
Addr_RegIm   = 0x5
Addr_DispReg = 0x6

# General Purpose Registers (4-bits)
Reg_RAX = Reg_EAX = Reg_AX = Reg_AL      = 0x0
Reg_RBX = Reg_EBX = Reg_BX = Reg_BL      = 0x1
Reg_RCX = Reg_ECX = Reg_CX = Reg_CL      = 0x2
Reg_RDX = Reg_EDX = Reg_DX = Reg_DL      = 0x3
Reg_RSI = Reg_ESI = Reg_SI = Reg_SIL     = 0x4
Reg_RDI = Reg_EDI = Reg_DI = Reg_DIL     = 0x5
Reg_RBP = Reg_EBP = Reg_BP = Reg_BPL     = 0x6
Reg_RSP = Reg_ESP = Reg_SP = Reg_SPL     = 0x7
Reg_R8 = Reg_R8D = Reg_R8W = Reg_R8B     = 0x8
Reg_R9 = Reg_R9D = Reg_R9W = Reg_R9B     = 0x9
Reg_R10 = Reg_R10D = Reg_R10W = Reg_R10B = 0xA
Reg_R11 = Reg_R11D = Reg_R11W = Reg_R11B = 0xB
Reg_R12 = Reg_R12D = Reg_R12W = Reg_R12B = 0xC
Reg_R13 = Reg_R13D = Reg_R13W = Reg_R13B = 0xD
Reg_R14 = Reg_R14D = Reg_R14W = Reg_R14B = 0xE
Reg_R15 = Reg_R15D = Reg_R15W = Reg_R15B = 0xF

# Floating Point Registers (4-bits)
SSE0 = EES0 = MMX0 = 0x0
SSE1 = EES1 = MMX1 = 0x1
SSE2 = EES2 = MMX2 = 0x2
SSE3 = EES3 = MMX3 = 0x3
SSE4 = EES4 = MMX4 = 0x4
SSE5 = EES5 = MMX5 = 0x5
SSE6 = EES6 = MMX6 = 0x6
SSE7 = EES7 = MMX7 = 0x7

# Extended Registers (4-bits)
ZMM0 = YMM0 = XMM0    = 0x0
ZMM1 = YMM1 = XMM1    = 0x1
ZMM2 = YMM2 = XMM2    = 0x2
ZMM3 = YMM3 = XMM3    = 0x3
ZMM4 = YMM4 = XMM4    = 0x4
ZMM5 = YMM5 = XMM5    = 0x5
ZMM6 = YMM6 = XMM6    = 0x6
ZMM7 = YMM7 = XMM7    = 0x7
ZMM8 = YMM8 = XMM8    = 0x8
ZMM9 = YMM9 = XMM9    = 0x9
ZMM10 = YMM10 = XMM10 = 0xA
ZMM11 = YMM11 = XMM11 = 0xB
ZMM12 = YMM12 = XMM12 = 0xC
ZMM13 = YMM13 = XMM13 = 0xD
ZMM14 = YMM14 = XMM14 = 0xE
ZMM15 = YMM15 = XMM15 = 0xF

# Instructions
MOV     = 0x88
CMOVG   = 0x4F
CMOVGE  = 0x4D
CMOVL   = 0x4C
CMOVLE  = 0x4E
CMOVE   = 0x44
CMOVNE  = 0x45
CMOVC   = 0x42
CMOVNC  = 0x43
CMOVO   = 0x40
CMOVNO  = 0x41
CMOVS   = 0x48
CMOVNS  = 0x49
CMOVP   = 0x4A
CMOVNP  = 0x4B
XCHG    = 0x91 # Swaps values from sources/destinations
BSWAP   = 0xC8 # Swaps endianess of destination
PUSH    = 0x0E
POP     = 0x07
ADD     = 0x00
ADC     = 0x14
SUB     = 0x2C
SBB     = 0x1C
MUL     = 0x69
IMUL    = 0x6B
DIV     = 0x50
IDIV    = 0x47
INC     = 0x46
DEC     = 0xFE
NEG     = 0xF7 # Two's Complement Negation
CMP     = 0x81
AND     = 0x24
OR      = 0x0C
XOR     = 0x30
NOT     = 0xF6 # One's Complement Negation
SHR     = 0xC3
SAR     = 0xC1
SHL     = 0xC0
SAL     = 0xC2
ROR     = 0xD3
ROL     = 0xD1
RCR     = 0xD0
RCL     = 0xD2
BT      = 0xA3 # BTR but keeps bit
BTS     = 0xBA # BTR but sets the bit to 1 instead of 0
BTR     = 0xB3 # Gets nth bit from location and clears it from location and puts it in CF
JMP     = 0xEB
JG      = 0x8F
JGE     = 0x8D
JL      = 0x8C
JLE     = 0x8E
JE      = 0x74
JNE     = 0x75
JERCXZ  = 0xE3
JC      = 0x72
JNC     = 0x73
JO      = 0x80
JNO     = 0x71
JS      = 0x78
JNS     = 0x79
JP      = 0x7A
JNP     = 0x7B
LOOP    = 0xE2
LOOPE   = 0xE1
LOOPNE  = 0xE0
CALL    = 0xFF
RET     = 0xCB
NOP     = 0xA0
CPUID   = 0xA2
HLT     = 0xF4
SYSCALL = 0xA5

Breakpoint = 0xCC
