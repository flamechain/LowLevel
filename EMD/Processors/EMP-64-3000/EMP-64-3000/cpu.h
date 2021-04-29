#pragma once
#include "emu.h"
#include "flags.h"
#include "ram.h"

constexpr auto INVALID_OPCODE = 0;
constexpr auto DOUBLE_FAULT = 1;

using namespace emu;

class CPU {
	DWord EAX;
	DWord EBX;
	DWord ECX;
	DWord EDX;
	DWord EDI;
	DWord ESI;
	DWord EBP;
	DWord ESP;

	DWord CR0;
	DWord CR1;
	DWord CR2;
	DWord CR3;
	DWord CR4;
	DWord CR5;
	DWord CR6;
	DWord CR7;

	DWord EIP;

	union {
		Byte PS;
		EFLAGS FLAGS;
	};

	Byte FetchByte();
	int RaiseException(int exception);

public:
	void Reset();
	void Boot();
	int Crash();
};
