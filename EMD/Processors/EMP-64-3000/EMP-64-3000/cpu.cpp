#include "cpu.h"
#include "codes.h"

extern RAM ram;

void CPU::Reset() {
	this->EAX = 0;
	this->EBX = 0;
	this->ECX = 0;
	this->EDX = 0;
	this->EDI = 0;
	this->ESI = 0;
	this->EBP = 0;
	this->ESP = 0;
	this->CR0 = 0;
	this->CR1 = 0;
	this->CR2 = 0;
	this->CR3 = 0;
	this->CR4 = 0;
	this->CR5 = 0;
	this->CR6 = 0;
	this->CR7 = 0;

	this->PS = 0;
	this->FLAGS.IF = 1;
	this->EIP = 0;
}

Byte CPU::FetchByte() {
	Byte value;
	
	if (!(this->EIP >= sizeof ram.data)) {
		value = ram.data[this->EIP++]; // uses current EIP then increments, "post-decrement"
	}
	else {
		value = ram.data[0];
		this->EIP = 1;
	}

	return value;
}

int CPU::RaiseException(int exception) {
	return 1;
}

void CPU::Boot() {
	while (true) {
		if (this->FLAGS.ST) {
			return;
		}

		Byte ins = this->FetchByte();

		switch (ins) {
		default:
			if (!this->RaiseException(INVALID_OPCODE)) {
				this->RaiseException(DOUBLE_FAULT);
			}

			break;
		}
	}
}

int CPU::Crash() {
	this->FLAGS.ST = 1;
	return this->EIP;
}
