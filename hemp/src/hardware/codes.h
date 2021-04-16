#ifndef CODES_H
#define CODES_H

int AddrReg             = 0;
int AddrIm              = 1;
int AddrDisp            = 2;
int AddrRegReg          = 3;
int AddrRegIm           = 4;
int AddrRegDisp         = 5;
int AddrDispReg         = 6;
int AddrDispIm          = 7;
int AddrDispDisp        = 8;
int AddrRegdispReg      = 9;
int AddrRegdispIm       = 10;
int AddrRegdispDisp     = 11;
int AddrRegdispRegdisp  = 12;
int AddrRegRegdisp      = 13;
int AddrDispRegdisp     = 14;
int AddrExtended        = 15;

int RegRAX, RegEAX, RegAX, RegAH, RegAL     = 0;
int RegRBX, RegEBX, RegBX, RegBH, RegBL     = 1;
int RegRCX, RegECX, RegCX, RegCH, RegCL     = 2;
int RegRDX, RegEDX, RegDX, RegDH, RegDL     = 3;
int RegRDI, RegEDI, RegDIX, RegDIH, RegDIL  = 4;
int RegRSI, RegESI, RegSIX, RegSIH, RegSIL  = 5;
int RegRBP, RegEBP, RegBPX, RegBPH, RegBPL  = 6;
int RegRSP, RegESP, RegSPX, RegSPH, RegSPL  = 7;
int RegR8, RegR8D, RegR8W, RegR8B           = 8;
int RegR9, RegR9D, RegR9W, RegR9B           = 9;
int RegR10, RegR10D, RegR10W, RegR10B       = 10;
int RegR11, RegR11D, RegR11W, RegR11B       = 11;
int RegR12, RegR12D, RegR12W, RegR12B       = 12;
int RegR13, RegR13D, RegR13W, RegR13B       = 13;
int RegR14, RegR14D, RegR14W, RegR14B       = 14;
int RegR15, RegR15D, RegR15W, RegR15B       = 15;

int RegCR0          = 16;
int RegCR1          = 17;
int RegCR2          = 18;
int RegCR3          = 19;
int RegCR4          = 20;
int RegCR5          = 21;
int RegCR6          = 22;
int RegCR7          = 23;
int RegF800, RegMMX0 = 24;
int RegF801, RegMMX1 = 25;
int RegF802, RegMMX2 = 26;
int RegF803, RegMMX3 = 27;
int RegF804, RegMMX4 = 28;
int RegF805, RegMMX5 = 29;
int RegF806, RegMMX6 = 30;
int RegF807, RegMMX7 = 31;

int ADD     = 0x00; // Add
int SUB     = 0x01; // Sub
int MUL     = 0x02; // Mul
int DIV     = 0x03; // Div
int ADC     = 0x04; // Add w/ Carry
int SBB     = 0x05; // Sub w/ Borrow (Carry)
int IMUL    = 0x06; // Signed Mul
int IDIV    = 0x07; // Signed Div
int FADD    = 0x08; // Float Add
int FSUB    = 0x09; // Float Sub 
int FMUL    = 0x0A; // Float Mul
int MDIV    = 0x0B; // Float Div
int RND     = 0x0C; // Round
int ABS     = 0x0D; // Abs
int FABS    = 0x0E; // Float Abs
int SIN     = 0x0F; // Sin
int COS     = 0x10; // Cos
int TAN     = 0x11; // Tan
int ASIN    = 0x12; // Sin-1
int ACOS    = 0x13; // Cos-1
int ATAN    = 0x14; // Tan-1
int CHS     = 0x15; // Change Sign
int SQRT    = 0x16; // Sqrt
int FSQRT   = 0x17; // Float Sqrt
int POW     = 0x18; // Power
int FPOW    = 0x19; // Float Power
int FLD     = 0x1A; // Float Load
int NEG     = 0x1B; // Two's Complement Negation
int NOT     = 0x1C; // One's Complement Negation
int AND     = 0x1D; // And
int OR      = 0x1E; // Or
int XOR     = 0x1F; // Xor
int BT      = 0x20; // Bit test
int BTC     = 0x21; // Bit test and complement
int BTR     = 0x22; // Bit test and reset
int BTS     = 0x23; // Bit test and set
int CBW     = 0x24; // Byte to word
int CWD     = 0x25; // Word to dword
int CDQ     = 0x26; // Dword to qword
int INC     = 0x27; // Inc
int DEC     = 0x28; // Dec
int ROL     = 0x29; // Rol
int ROR     = 0x2A; // Ror
int RCL     = 0x2B; // Rcl
int RCR     = 0x2C; // Rcr
int SHL     = 0x2D; // Shl
int SHR     = 0x2E; // Shr
int SAL     = 0x2F; // Sal
int SAR     = 0x30; // Sar
int TST     = 0x31; // Test
int FTST    = 0x32; // Float test
int FLDZ    = 0x33; // Float load zero
int FLD1    = 0x34; // Float load one
int FLDPI   = 0x35; // Float load pi
int BTSWAP  = 0x36; // Exchange bytes (endian change)
int STC     = 0x37; // Set carry flag
int CTC     = 0x38; // Clear carry flag
int CMC     = 0x39; // Complement carry flag
int STD     = 0x3A; // Set direction flag
int CLD     = 0x3B; // Clear direction flag
int STI     = 0x3C; // Set interrupt enable flag
int CLI     = 0x3D; // Clear interrupt enable flag
int CMP     = 0x3F; // Cmp
int FCMP    = 0x40; // Float cmp
int MOV     = 0x41; // Mov
int CMOVB   = 0x42; // Cmov below               (CF=1)
int CMOVBE  = 0x43; // Cmov below equal         (CF=1 or ZF=1)
int CMOVA   = 0x44; // Cmov above               (CF=0 and ZF=0)
int CMOVAE  = 0x45; // Cmov above equal         (CF=0)
int CMOVG   = 0x46; // Cmov greater             (ZF=0 and SF=OF)
int CMOVGE  = 0x47; // Cmov greater equal       (SF=OF)
int CMOVL   = 0x48; // Cmov lesser              (SF!=OF)
int CMOVLE  = 0x49; // Cmov lesser equal        (ZF=1 or SF!=OF)
int CMOVE   = 0x4A; // Cmov equal               (ZF=1)
int CMOVNE  = 0x4B; // Cmov not equal           (ZF=0)
int CMOVC   = 0x4C; // Cmov carry flag
int CMOVNC  = 0x4D; // Cmov not carry flag
int CMOVO   = 0x4E; // Cmov overflow flag
int CMOVNO  = 0x4F; // Cmov not overflow flag
int CMOVS   = 0x50; // Cmov sign flag
int CMOVNS  = 0x51; // Cmov not sign flag
int CMOVP   = 0x52; // Cmov parity flag
int CMOVNP  = 0x53; // Cmov not parity flag
int JMP     = 0x54; // Jmp
int JA      = 0x55; // Jmp above
int JAE     = 0x56; // Jmp above equal
int JB      = 0x57; // Jmp below
int JBE     = 0x58; // Jmp below equal
int JG      = 0x59; // Jmp greater
int JGE     = 0x5A; // Jmp greater equal
int JL      = 0x5B; // Jmp lesser
int JLE     = 0x5C; // Jmp lesser equal
int JE      = 0x5D; // Jmp equal
int JNE     = 0x5E; // Jmp not equal
int JERCXZ  = 0x5F; // Jmp if RCX/ECX/CX is zero
int JC      = 0x60; // Jmp carry flag
int JNC     = 0x61; // Jmp not carry flag
int JO      = 0x62; // Jmp overflow flag
int JNO     = 0x63; // Jmp not overflow flag
int JS      = 0x64; // Jmp sign flag
int JNS     = 0x65; // Jmp not sign flag
int JP      = 0x66; // Jmp parity flag
int JNP     = 0x67; // Jmp not parity flag
int LOOP    = 0x68; // Loop
int LOOPE   = 0x69; // Loop equal
int LOOPNE  = 0x6A; // Loop not equal
int CALL    = 0x6B; // Call
int RET     = 0x6C; // Ret
int NOP     = 0x6D; // Nop
int UD      = 0x6E; // Ud
int HLT     = 0x6F; // Hlt
int CPUID   = 0x70; // Cpuid
int SYSCALL = 0x71; // Syscall
int INT     = 0x72; // Interrupt
int POP     = 0x73; // Pop
int POPA    = 0x74; // Pop all registers
int POPF    = 0x75; // Pop flags
int POPFD   = 0x76; // Pop eflags
int POPFQ   = 0x77; // Pop rflags
int PUSH    = 0x78; // Push
int PUSHA   = 0x79; // Push all registers
int PUSHF   = 0x7A; // Push flags
int PUSHFD  = 0x7B; // Push eflags
int PUSHFQ  = 0x7C; // Push rflags
int RDMSR   = 0x7D; // Read from model specific register
int WRMSR   = 0x7E; // Write to model specific register
int LGDT    = 0x7F; // Load globa descriptor table
int SGDT    = 0x80; // Set globa descriptor table
int RDPID   = 0x81; // Read processor ID
int LLDT    = 0x82; // Load local descriptor table
int SLDT    = 0x83; // Set local descriptor table
int WAIT    = 0x84; // Check floating point exceptions
int MONITOR = 0x85; // Change visual memory
int OUT     = 0x86; // Out port
int IN      = 0x87; // In port
int LAHF    = 0x88; // Load Flags
int SAHF    = 0x89; // Store Flags
int MOVS    = 0x8A; // Mov string
int CMPS    = 0x8B; // Cmp string
int SCAS    = 0x8C; // Scan string
int LODS    = 0x8D; // Load string
int STOS    = 0x8E; // Store string
int SETB    = 0x8F; // Set below
int SETBE   = 0x90; // Set below equal
int SETA    = 0x91; // Set above
int SETAE   = 0x92; // Set above equal
int SETG    = 0x93; // Set greater
int SETGE   = 0x94; // Set greater equal
int SETL    = 0x95; // Set lesser
int SETLE   = 0x96; // Set lesser equal
int SETE    = 0x97; // Set equal
int SETNE   = 0x98; // Set not equal
int SETC    = 0x99; // Set carry flag
int SETNC   = 0x9A; // Set not carry flag
int SETO    = 0x9B; // Set overflow flag
int SETNO   = 0x9C; // Set not overflow flag
int SETS    = 0x9D; // Set sign flag
int SETNS   = 0x9E; // Set not sign flag
int SETP    = 0x9F; // Set parity flag
int SETNP   = 0xA0; // Set not parity flag
int IRET    = 0xA1; // Iret?
int LOOP    = 0xA2; // Loop
int LOOPE   = 0xA3; // Loop equal               (count != 0 and ZF = 1)
int LOOPNE  = 0xA4; // Loop not equal           (count != 0 and ZF = 0)


int Breakpoint = 0x3E;

int prefixes[] = {
    0x66, // Operand-size prefix
    0x67, // Address-size prefix
    0xF2,
    0xF3
};

#endif
