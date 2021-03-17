#pragma once
#include "Memory.h"
#include "definitions.h"

using Byte = unsigned char;
using Word = unsigned short;
using uint = unsigned int;

class CPU {

	struct StatusFlags {
		Byte C : 1; // Carry
		Byte Z : 1; // Zero
		Byte I : 1; // Interupt Disable
		Byte T : 1; // Trap / Single-step
		Byte B : 1; // Break
		Byte O : 1; // Overflow
		Byte N : 1; // Negative
		Byte U : 1; // Unsused
	};

public:

	Word NMI;
	Word IRQ;
	Word PC;
	Byte SP;

	Byte EAX, EBX, ECX, EDX;

	Memory mem;
	uint cycles;

	union {
		Byte FullPS;
		StatusFlags PS;
	};

	static constexpr Byte
		NOP     = 0x01,
		RTS     = 0x23,
		STA_ABS = 0x31,
		ROR_AC  = 0x1E,
		JMP_ABS = 0xE0,
		JSR     = 0xE2,
		LDA_IM  = 0xE8;

	void Reset(Word rVector = 0x8000, Word nmiVector = 0x0000, Word irqVector = 0x0000);
	uint Execute(int cycles);

	Word SPToWord();
	void SetFlags_ZN(Byte value);
	Byte ROR(Byte value);
	void PushPCToStack();
	Word PopWordFromStack();

	Word AddrAbsolute();

	Byte ReadByte(Word address);
	Word ReadWord(Word address);
	void WriteByte(Byte value, Word address);
	void WriteWord(Word value, Word address);
	Byte FetchByte();
	Word FetchWord();
};
