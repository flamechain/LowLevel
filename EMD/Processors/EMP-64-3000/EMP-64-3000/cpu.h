#pragma once

#include "emu.h"
#include "rflags.h"
#include "codes.h"
#include "ram.h"

using namespace emu;

class CPU {
	QWord RAX;
	QWord RBX;
	QWord RCX;
	QWord RDX;
	QWord RDI;
	QWord RSI;
	QWord RBP;
	QWord RSP;
	QWord R8;
	QWord R9;
	QWord R10;
	QWord R11;
	QWord R12;
	QWord R13;
	QWord R14;
	QWord R15;

	QWord CR0;
	QWord CR1;
	QWord CR2;
	QWord CR3;
	QWord CR4;
	QWord CR5;
	QWord CR6;
	QWord CR7;

	FExtend SSE0;
	FExtend SSE1;
	FExtend SSE2;
	FExtend SSE3;
	FExtend SSE4;
	FExtend SSE5;
	FExtend SSE6;
	FExtend SSE7;

	FDouble MMX0;
	FDouble MMX1;
	FDouble MMX2;
	FDouble MMX3;
	FDouble MMX4;
	FDouble MMX5;
	FDouble MMX6;
	FDouble MMX7;

	DQWord XMM0;
	DQWord XMM1;
	DQWord XMM2;
	DQWord XMM3;
	DQWord XMM4;
	DQWord XMM5;
	DQWord XMM6;
	DQWord XMM7;

	QWord RIP;

	union {
		Byte PS;
		RFLAGS FLAGS;
	};

	int InvalidOpcode = 1;

	Byte FetchByte();
	void RaiseException(int exception, int context[]);

public:
	void Reset();
	void Boot();
	int Crash();
};
