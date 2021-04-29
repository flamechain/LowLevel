#pragma once
#include "emu.h"

using namespace emu;

Byte ADD	= 0x00; // Addition
Byte SUB	= 0x01; // Subtraction
Byte MUL	= 0x02; // Multiplication
Byte DIV	= 0x03; // Division
Byte ADC	= 0x04; // Addition with Carry
Byte SBB	= 0x05; // Subtraction with Borrow
Byte ABS	= 0x06; // Absolute value
Byte CHS	= 0x07; // Change Sign
Byte NEG	= 0x08; // Two's Complement Negation
Byte NOT	= 0x09; // One's Complement Negation
Byte AND	= 0x0A; // And
Byte OR		= 0x0B; // Or
Byte XOR	= 0x0C; // Xor
Byte BT		= 0x0D; // Bit test
Byte BTC	= 0x0E; // Bit test and complement
Byte BTR	= 0x0F; // Bit test and reset
Byte BTS	= 0x10; // Bit test and set
Byte CBW	= 0x11; // Byte to word
Byte CWD	= 0x12; // Word to dword
Byte INC	= 0x13; // Inccrement
Byte DEC	= 0x14; // Decrement
Byte ROL	= 0x15; // Rotate left
Byte ROR	= 0x16; // Rotate right
Byte RCL	= 0x17; // Rotate carry right
Byte RCR	= 0x18; // Rotate carry left
Byte SHL	= 0x19; // Shift logical left
Byte SHR	= 0x1A; // Shift logical right
Byte SAL	= 0x1B; // Shift arithmetic right
Byte SAR	= 0x1C; // Shift arithmetic left
Byte TST	= 0x1D; // Test
Byte BTSWAP = 0x1E; // Exchange bytes (endian change)
Byte STC	= 0x1F; // Set carry flag
Byte CTC	= 0x20; // Clear carry flag
Byte CMC	= 0x21; // Complement carry flag
Byte STD	= 0x22; // Set direction flag
Byte CLD	= 0x23; // Clear direction flag
Byte STI	= 0x24; // Set interrupt enable flag
Byte CLI	= 0x25; // Clear interrupt enable flag
Byte CMP	= 0x26; // Compare
Byte MOV	= 0x27; // Move
Byte CMOVB	= 0x28; // Conditional move below               (CF=1)
Byte CMOVBE = 0x29; // Conditional move below equal         (CF=1 or ZF=1)
Byte CMOVA	= 0x2A; // Conditional move above               (CF=0 and ZF=0)
Byte CMOVAE = 0x2B; // Conditional move above equal         (CF=0)
Byte CMOVG	= 0x2C; // Conditional move greater             (ZF=0 and SF=OF)
Byte CMOVGE = 0x2D; // Conditional move greater equal       (SF=OF)
Byte CMOVL	= 0x2E; // Conditional move lesser              (SF!=OF)
Byte CMOVLE = 0x2F; // Conditional move lesser equal        (ZF=1 or SF!=OF)
Byte CMOVE	= 0x30; // Conditional move equal               (ZF=1)
Byte CMOVNE = 0x31; // Conditional move not equal           (ZF=0)
Byte CMOVC	= 0x32; // Conditional move carry flag
Byte CMOVNC = 0x33; // Conditional move not carry flag
Byte CMOVO	= 0x34; // Conditional move overflow flag
Byte CMOVNO = 0x35; // Conditional move not overflow flag
Byte CMOVS	= 0x36; // Conditional move sign flag
Byte CMOVNS = 0x37; // Conditional move not sign flag
Byte CMOVP	= 0x38; // Conditional move parity flag
Byte CMOVNP = 0x39; // Conditional move not parity flag
Byte JMP	= 0x3A; // Jump
Byte JA		= 0x3B; // Jump above
Byte JAE	= 0x3C; // Jump above equal
Byte JB		= 0x3D; // Jump below
Byte JBE	= 0x3E; // Jump below equal
Byte JG		= 0x3F; // Jump greater
Byte JGE	= 0x40; // Jump greater equal
Byte JL		= 0x41; // Jump lesser
Byte JLE	= 0x42; // Jump lesser equal
Byte JE		= 0x43; // Jump equal
Byte JNE	= 0x44; // Jump not equal
Byte JECXZ	= 0x45; // Jump if ECX/CX is zero
Byte JC		= 0x46; // Jump carry flag
Byte JNC	= 0x47; // Jump not carry flag
Byte JO		= 0x48; // Jump overflow flag
Byte JNO	= 0x49; // Jump not overflow flag
Byte JS		= 0x4A; // Jump sign flag
Byte JNS	= 0x4B; // Jump not sign flag
Byte JP		= 0x4C; // Jump parity flag
Byte JNP	= 0x4D; // Jump not parity flag
Byte LOOP	= 0x4E; // Loop
Byte LOOPE	= 0x4F; // Loop equal               (count != 0 and ZF = 1)
Byte LOOPNE = 0x50; // Loop not equal           (count != 0 and ZF = 0)
Byte CALL	= 0x51; // Call
Byte RET	= 0x52; // Return
Byte NOP	= 0x53; // No Operation
Byte UD		= 0x54; // Undefined Opcode
Byte HLT	= 0x55; // Halt
Byte CPUID	= 0x56; // CPU ID
Byte _INT	= 0x57; // Interrupt
Byte POP	= 0x58; // Pop
Byte POPA	= 0x59; // Pop all registers
Byte POPF	= 0x5A; // Pop flags
Byte POPFD	= 0x5B; // Pop eflags
Byte PUSH	= 0x5C; // Push
Byte PUSHA	= 0x5D; // Push all registers
Byte PUSHF	= 0x5E; // Push flags
Byte PUSHFD = 0x5F; // Push eflags
Byte _OUT	= 0x60; // Out port
Byte _IN	= 0x61; // In port
