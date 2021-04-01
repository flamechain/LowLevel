Size64 = 0b1000 << 4
Size32 = 0b1001 << 4
Size16 = 0b1010 << 4
Size8  = 0b1011 << 4

AddrRegIm   = 0
AddrReg     = 1
AddrIm      = 2
AddrDisp    = 3
AddrRegReg  = 4
AddrRegDisp = 5
AddrDispReg = 6
AddrDispIm  = 7

CodeRAX = 0
CodeRBX = 1
CodeRCX = 2
CodeRDX = 3
CodeRDI = 4
CodeRSI = 5
CodeRBP = 6
CodeRSP = 7
CodeR8  = 8
CodeR9  = 9
CodeR10 = 10
CodeR11 = 11
CodeR12 = 12
CodeR13 = 13
CodeR14 = 14
CodeR15 = 15

NOP         = 0x00
UD          = 0x01
HLT         = 0x02
INT         = 0x03
CPUID       = 0x07
SYSEXIT     = 0x0B
Breakpoint  = 0xCC

MOV         = 0x04

PUSH        = 0x05
POP         = 0x06

CALL        = 0x08
RET         = 0x09
JMP         = 0x0A

CMP         = 0x0C
JNE         = 0x0D

# Required for OS:

# jb
# jz
# je
# popfd
# pushfd
# or
# inc
# test
# rdmsr
# wrmsr
# lgdt
