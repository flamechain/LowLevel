#include "windows.h"

using DWord = unsigned int;
using Byte = unsigned char;

void DrawRect(HDC hdc, int x, int y, int width, int height, HBRUSH hbr) {
	RECT rect = RECT();
	rect.left = x;
	rect.top = y;
	rect.right = x + width;
	rect.bottom = y + height;
    HRGN rgn = CreateRectRgnIndirect(&rect);
	FillRgn(hdc, rgn, hbr);
}

void EnterFullscreen(HWND hwnd) {
    DWord dwStyle = ::GetWindowLong(hwnd, GWL_STYLE);
    DWord dwRemove = WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX;
    DWord dwNewStyle = dwStyle & ~dwRemove;
    ::SetWindowLong(hwnd, GWL_STYLE, dwNewStyle);
    ::SetWindowPos(hwnd, NULL, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED);
    HDC hdc = ::GetWindowDC(NULL);
    ::SetWindowPos(hwnd, NULL, 0, 0, ::GetDeviceCaps(hdc, HORZRES), ::GetDeviceCaps(hdc, VERTRES), SWP_FRAMECHANGED);
}

//case WM_LBUTTONDOWN:
//    OutputDebugStringW(L"LButtonDown\n");
//    break;
//case WM_LBUTTONUP:
//    OutputDebugStringW(L"LButtonUp\n");
//    break;
//case WM_MBUTTONDOWN:
//    OutputDebugStringW(L"MButtonDown\n");
//    break;
//case WM_MBUTTONUP:
//    OutputDebugStringW(L"MButtonUp\n");
//    break;
//case WM_RBUTTONDOWN:
//    OutputDebugStringW(L"RButtonDown\n");
//    break;
//case WM_RBUTTONUP:
//    OutputDebugStringW(L"RButtonUp\n");
//    break;

Byte ADD = 0x00; // Add
Byte SUB = 0x01; // Sub
Byte MUL = 0x02; // Mul
Byte DIV = 0x03; // Div
Byte ADC = 0x04; // Add w/ Carry
Byte SBB = 0x05; // Sub w/ Borrow (Carry)
Byte IMUL = 0x06; // Signed Mul
Byte IDIV = 0x07; // Signed Div
Byte FADD = 0x08; // Float Add
Byte FSUB = 0x09; // Float Sub 
Byte FMUL = 0x0A; // Float Mul
Byte MDIV = 0x0B; // Float Div
Byte RND = 0x0C; // Round
Byte ABS = 0x0D; // Abs
Byte FABS = 0x0E; // Float Abs
Byte SIN = 0x0F; // Sin
Byte COS = 0x10; // Cos
Byte TAN = 0x11; // Tan
Byte ASIN = 0x12; // Sin-1
Byte ACOS = 0x13; // Cos-1
Byte ATAN = 0x14; // Tan-1
Byte CHS = 0x15; // Change Sign
Byte SQRT = 0x16; // Sqrt
Byte FSQRT = 0x17; // Float Sqrt
Byte POW = 0x18; // Power
Byte FPOW = 0x19; // Float Power
Byte FLD = 0x1A; // Float Load
Byte NEG = 0x1B; // Two's Complement Negation
Byte NOT = 0x1C; // One's Complement Negation
Byte AND = 0x1D; // And
Byte OR = 0x1E; // Or
Byte XOR = 0x1F; // Xor
Byte BT = 0x20; // Bit test
Byte BTC = 0x21; // Bit test and complement
Byte BTR = 0x22; // Bit test and reset
Byte BTS = 0x23; // Bit test and set
Byte CBW = 0x24; // Byte to word
Byte CWD = 0x25; // Word to dword
Byte CDQ = 0x26; // Dword to qword
Byte INC = 0x27; // Inc
Byte DEC = 0x28; // Dec
Byte ROL = 0x29; // Rol
Byte ROR = 0x2A; // Ror
Byte RCL = 0x2B; // Rcl
Byte RCR = 0x2C; // Rcr
Byte SHL = 0x2D; // Shl
Byte SHR = 0x2E; // Shr
Byte SAL = 0x2F; // Sal
Byte SAR = 0x30; // Sar
Byte TST = 0x31; // Test
Byte FTST = 0x32; // Float test
Byte FLDZ = 0x33; // Float load zero
Byte FLD1 = 0x34; // Float load one
Byte FLDPI = 0x35; // Float load pi
Byte BTSWAP = 0x36; // Exchange bytes (endian change)
Byte STC = 0x37; // Set carry flag
Byte CTC = 0x38; // Clear carry flag
Byte CMC = 0x39; // Complement carry flag
Byte STD = 0x3A; // Set direction flag
Byte CLD = 0x3B; // Clear direction flag
Byte STI = 0x3C; // Set interrupt enable flag
Byte CLI = 0x3D; // Clear interrupt enable flag
Byte CMP = 0x3F; // Cmp
Byte FCMP = 0x40; // Float cmp
Byte MOV = 0x41; // Mov
Byte CMOVB = 0x42; // Cmov below               (CF=1)
Byte CMOVBE = 0x43; // Cmov below equal         (CF=1 or ZF=1)
Byte CMOVA = 0x44; // Cmov above               (CF=0 and ZF=0)
Byte CMOVAE = 0x45; // Cmov above equal         (CF=0)
Byte CMOVG = 0x46; // Cmov greater             (ZF=0 and SF=OF)
Byte CMOVGE = 0x47; // Cmov greater equal       (SF=OF)
Byte CMOVL = 0x48; // Cmov lesser              (SF!=OF)
Byte CMOVLE = 0x49; // Cmov lesser equal        (ZF=1 or SF!=OF)
Byte CMOVE = 0x4A; // Cmov equal               (ZF=1)
Byte CMOVNE = 0x4B; // Cmov not equal           (ZF=0)
Byte CMOVC = 0x4C; // Cmov carry flag
Byte CMOVNC = 0x4D; // Cmov not carry flag
Byte CMOVO = 0x4E; // Cmov overflow flag
Byte CMOVNO = 0x4F; // Cmov not overflow flag
Byte CMOVS = 0x50; // Cmov sign flag
Byte CMOVNS = 0x51; // Cmov not sign flag
Byte CMOVP = 0x52; // Cmov parity flag
Byte CMOVNP = 0x53; // Cmov not parity flag
Byte JMP = 0x54; // Jmp
Byte JA = 0x55; // Jmp above
Byte JAE = 0x56; // Jmp above equal
Byte JB = 0x57; // Jmp below
Byte JBE = 0x58; // Jmp below equal
Byte JG = 0x59; // Jmp greater
Byte JGE = 0x5A; // Jmp greater equal
Byte JL = 0x5B; // Jmp lesser
Byte JLE = 0x5C; // Jmp lesser equal
Byte JE = 0x5D; // Jmp equal
Byte JNE = 0x5E; // Jmp not equal
Byte JERCXZ = 0x5F; // Jmp if RCX/ECX/CX is zero
Byte JC = 0x60; // Jmp carry flag
Byte JNC = 0x61; // Jmp not carry flag
Byte JO = 0x62; // Jmp overflow flag
Byte JNO = 0x63; // Jmp not overflow flag
Byte JS = 0x64; // Jmp sign flag
Byte JNS = 0x65; // Jmp not sign flag
Byte JP = 0x66; // Jmp parity flag
Byte JNP = 0x67; // Jmp not parity flag
Byte LOOP = 0xA2; // Loop
Byte LOOPE = 0xA3; // Loop equal               (count != 0 and ZF = 1)
Byte LOOPNE = 0xA4; // Loop not equal           (count != 0 and ZF = 0)
Byte CALL = 0x6B; // Call
Byte RET = 0x6C; // Ret
Byte NOP = 0x6D; // Nop
Byte UD = 0x6E; // Ud
Byte HLT = 0x6F; // Hlt
Byte CPUID = 0x70; // Cpuid
Byte SYSCALL = 0x71; // Syscall
Byte _INT = 0x72; // Interrupt
Byte POP = 0x73; // Pop
Byte POPA = 0x74; // Pop all registers
Byte POPF = 0x75; // Pop flags
Byte POPFD = 0x76; // Pop eflags
Byte POPFQ = 0x77; // Pop rflags
Byte PUSH = 0x78; // Push
Byte PUSHA = 0x79; // Push all registers
Byte PUSHF = 0x7A; // Push flags
Byte PUSHFD = 0x7B; // Push eflags
Byte PUSHFQ = 0x7C; // Push rflags
Byte RDMSR = 0x7D; // Read from model specific register
Byte WRMSR = 0x7E; // Write to model specific register
Byte LGDT = 0x7F; // Load globa descriptor table
Byte SGDT = 0x80; // Set globa descriptor table
Byte RDPID = 0x81; // Read processor ID
Byte LLDT = 0x82; // Load local descriptor table
Byte SLDT = 0x83; // Set local descriptor table
Byte WAIT = 0x84; // Check floating poByte exceptions
Byte MONITOR = 0x85; // Change visual memory
Byte _OUT = 0x86; // Out port
Byte _IN = 0x87; // In port
Byte LAHF = 0x88; // Load Flags
Byte SAHF = 0x89; // Store Flags
Byte MOVS = 0x8A; // Mov string
Byte CMPS = 0x8B; // Cmp string
Byte SCAS = 0x8C; // Scan string
Byte LODS = 0x8D; // Load string
Byte STOS = 0x8E; // Store string
Byte SETB = 0x8F; // Set below
Byte SETBE = 0x90; // Set below equal
Byte SETA = 0x91; // Set above
Byte SETAE = 0x92; // Set above equal
Byte SETG = 0x93; // Set greater
Byte SETGE = 0x94; // Set greater equal
Byte SETL = 0x95; // Set lesser
Byte SETLE = 0x96; // Set lesser equal
Byte SETE = 0x97; // Set equal
Byte SETNE = 0x98; // Set not equal
Byte SETC = 0x99; // Set carry flag
Byte SETNC = 0x9A; // Set not carry flag
Byte SETO = 0x9B; // Set overflow flag
Byte SETNO = 0x9C; // Set not overflow flag
Byte SETS = 0x9D; // Set sign flag
Byte SETNS = 0x9E; // Set not sign flag
Byte SETP = 0x9F; // Set parity flag
Byte SETNP = 0xA0; // Set not parity flag
Byte IRET = 0xA1; // Iret?
Byte BREAKPOINT = 0x3E;
