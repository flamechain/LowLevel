#pragma once

#include "emu.h"

using namespace emu;

class RFLAGS {
public:
	Byte CF    : 1; // Carry Flag
	Byte Res1  : 1;
	Byte PF    : 1; // Parity Flag
	Byte Res3  : 1;
	Byte AF	   : 1; // Auxilary carry Flag
	Byte Res5  : 1;
	Byte ZF	   : 1; // Zero Flag
	Byte SF	   : 1; // Sign Flag
	Byte TF	   : 1; // Trap Flag (single-step)
	Byte IF	   : 1; // Interrupt enable Flag
	Byte DF	   : 1; // Direction Flag
	Byte OF	   : 1; // Overflow Flag
	Byte IOPL  : 2; // I/O Privilage Level field
	Byte NT	   : 1; // Nested Task flag
	Byte Res15 : 1;
	Byte RF	   : 1; // Resume Flag
	Byte VM	   : 1; // Virtual-64 Mode flag
	Byte AC	   : 1; // Alignment Check flag
	Byte VIF   : 1; // Virtual Interrupt Flag
	Byte VIP   : 1; // Virtual Interrupt Pending flag
	Byte ID	   : 1; // ID
	Byte Res22 : 1;
	Byte ST	   : 1; // Assert STOP signal
	Byte Res24 : 8;
	DWord Res32: 32;
};

class EFLAGS {
public:
	Byte CF : 1; // Carry Flag
	Byte Res1 : 1;
	Byte PF : 1; // Parity Flag
	Byte Res3 : 1;
	Byte AF : 1; // Auxilary carry Flag
	Byte Res5 : 1;
	Byte ZF : 1; // Zero Flag
	Byte SF : 1; // Sign Flag
	Byte TF : 1; // Trap Flag (single-step)
	Byte IF : 1; // Interrupt enable Flag
	Byte DF : 1; // Direction Flag
	Byte OF : 1; // Overflow Flag
	Byte IOPL : 2; // I/O Privilage Level field
	Byte NT : 1; // Nested Task flag
	Byte Res15 : 1;
	Byte RF : 1; // Resume Flag
	Byte VM : 1; // Virtual-32 Mode flag
	Byte AC : 1; // Alignment Check flag
	Byte VIF : 1; // Virtual Interrupt Flag
	Byte VIP : 1; // Virtual Interrupt Pending flag
	Byte ID : 1; // ID
	Byte Res22 : 1;
	Byte ST : 1; // Assert STOP signal
	Byte Res24 : 8;
};
