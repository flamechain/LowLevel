#include "cpu.h"

extern RAM ram;

void CPU::Reset() {
	this->RAX = 0;
	this->RBX = 0;
	this->RCX = 0;
	this->RDX = 0;
	this->RDI = 0;
	this->RSI = 0;
	this->RBP = 0;
	this->RSP = 0;
	this->R8 = 0;
	this->R9 = 0;
	this->R10 = 0;
	this->R11 = 0;
	this->R12 = 0;
	this->R13 = 0;
	this->R14 = 0;
	this->R15 = 0;
	this->CR0 = 0;
	this->CR1 = 0;
	this->CR2 = 0;
	this->CR3 = 0;
	this->CR4 = 0;
	this->CR5 = 0;
	this->CR6 = 0;
	this->CR7 = 0;
	this->SSE0 = 0;
	this->SSE1 = 0;
	this->SSE2 = 0;
	this->SSE3 = 0;
	this->SSE4 = 0;
	this->SSE5 = 0;
	this->SSE6 = 0;
	this->SSE7 = 0;
	this->MMX0 = 0;
	this->MMX1 = 0;
	this->MMX2 = 0;
	this->MMX3 = 0;
	this->MMX4 = 0;
	this->MMX5 = 0;
	this->MMX6 = 0;
	this->MMX7 = 0;
	this->XMM0 = 0;
	this->XMM1 = 0;
	this->XMM2 = 0;
	this->XMM3 = 0;
	this->XMM4 = 0;
	this->XMM5 = 0;
	this->XMM6 = 0;
	this->XMM7 = 0;

	this->PS = 0;
	this->FLAGS.IF = 1;
	this->RIP = 0;
}

Byte CPU::FetchByte() {
	Byte value = ram.data[this->RIP++]; // uses current RIP then increments, "post-decrement"
	return value;
}

void CPU::RaiseException(int exception, int context[]) {

}

void CPU::Boot() {
	while (true) {
		if (this->FLAGS.ST) {
			return;
		}

		Byte ins = this->FetchByte();

		switch (ins) {
		case 1:
			OutputDebugStringW(L"1 was the instruction\n");
		default:
			OutputDebugStringW(L"unknown instruction\n");
			this->RaiseException(this->InvalidOpcode, {(int *)ins});
			break;
		}
	}
}

int CPU::Crash() {
	this->FLAGS.ST = 1;
	return this->RIP;
}
