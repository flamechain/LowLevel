RegEAX = RegAX = RegAH = RegAL = 0
RegEBX = RegBX = RegBH = RegBL = 1
RegECX = RegCX = RegCH = RegCL = 2
RegEDX = RegDX = RegDH = RegDL = 3
RegEDI = RegDI = 4
RegESI = RegSI = 5
RegEBP = RegBP = 6
RegESP = RegSP = 7

ModReg              = 0x0
ModIm               = 0x1
ModDisp             = 0x2
ModRegDisp          = 0x3
ModRegReg           = 0x4
ModRegIm            = 0x5
ModDispReg          = 0x6
ModDispIm           = 0x7
ModDispDisp         = 0x8
ModRegdispReg       = 0x9
ModRegdispRegdisp   = 0xa

Size8   = 0
Size16  = 1
Size32  = 2

JMP     = 0x02 # ModIm
CALL    = 0x05 # ModIm
PUSH    = 0x0D # ModReg, ModIm
POP     = 0x0C # ModReg
MOV     = 0x01 # ModRegIm, ModDispReg, ModDispIm, ModDispDisp, ModRegdispReg, ModRegdispRegdisp
ADD     = 0x00 # ModRegReg
MUL     = 0x08 # ModRegIm, ModRegReg
OR      = 0x09 # ModRegIm
XOR     = 0x0A # ModRegReg
CMP     = 0x03 # ModRegIm
JE      = 0x04 # ModIm
SAL     = 0x0B # ModRegIm
RET     = 0x06 #
INC     = 0x07 # ModReg
SHUTDWN = 0x0E #
