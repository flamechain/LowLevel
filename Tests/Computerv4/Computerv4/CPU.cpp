#include <iostream>
#include "CPU.h"

void CPU::Reset(Word rVector, Word nmiVector, Word irqVector) {
	this->EAX = 0x00;
	this->EBX = 0x00;
	this->ECX = 0x00;
	this->EDX = 0x00;

	this->SP = 0xFF;

	this->mem.Data[0xFFFA] = (nmiVector & 0xFF00) >> 8;
	this->mem.Data[0xFFFB] = nmiVector & 0xFF;
	this->mem.Data[0xFFFC] = (rVector & 0xFF00) >> 8;
	this->mem.Data[0xFFFD] = rVector & 0xFF;
	this->mem.Data[0xFFFE] = (irqVector & 0xFF00) >> 8;
	this->mem.Data[0xFFFF] = irqVector & 0xFF;

	this->PC = (this->mem.Data[0xFFFC] << 8) | this->mem.Data[0xFFFD];
	this->NMI = (this->mem.Data[0xFFFA] << 8) | this->mem.Data[0xFFFB];
	this->IRQ = (this->mem.Data[0xFFFE] << 8) | this->mem.Data[0xFFFF];
}

void CPU::WriteByte(Byte value, Word address) {
	this->mem.Data[address] = value;
	this->cycles--;
}

void CPU::WriteWord(Word value, Word address) {
	throw - 1;
}

Byte CPU::FetchByte() {
	Byte value = this->mem.Data[this->PC];
	this->PC++;
	this->cycles--;

	return value;
}

Word CPU::FetchWord() {
	Word value = this->mem.Data[this->PC] << 8;
	this->PC++;
	value |= this->mem.Data[this->PC];
	this->PC++;
	this->cycles -= 2;

	return value;
}

Byte CPU::ReadByte(Word address) {
	Byte value = this->mem.Data[address];
	this->cycles--;

	return value;
}

Word CPU::ReadWord(Word address) {
	Byte LoByte = this->ReadByte(address);
	Byte HiByte = this->ReadByte(address + 1);

	return LoByte | (HiByte << 8);
}

void CPU::SetFlags_ZN(Byte value) {
	this->PS.Z = (value == 0);
	this->PS.N = (value & 0b10000000) > 0;
}

Word CPU::AddrAbsolute() {
	return this->FetchWord();
}

Byte CPU::ROR(Byte value) {
	Byte bit7 = this->PS.C;
	this->PS.C = (value & 1);
	value = (value >> 1) & 0xFF;
	value |= (bit7 << 7);
	this->SetFlags_ZN(value);
	this->cycles--;

	return value;
}

Word CPU::SPToWord() {
	return 0x0100 | this->SP;
}

void CPU::PushPCToStack() {
	this->WriteByte(this->PC >> 8, this->SPToWord());
	this->SP--;
	this->PC--;
	this->WriteByte(this->PC & 0xFF, this->SPToWord());
	this->SP--;
}

Word CPU::PopWordFromStack() {
	Word value = this->ReadWord(this->SPToWord() + 1);
	this->SP += 2;
	this->cycles--;

	return value;
}

uint CPU::Execute(int cycles) {
	this->cycles = cycles;
	Word Address = 0;

	while (this->cycles > 0) {
		Byte Ins = this->FetchByte();

		switch (Ins) {
		case this->NOP:
			this->cycles--;
		    break;
		case this->LDA_IM:
			this->EAX = this->FetchByte();
			this->SetFlags_ZN(this->EAX);
			break;
		case this->STA_ABS:
			Address = this->AddrAbsolute();
			this->WriteByte(this->EAX, Address);
			break;
		case this->JMP_ABS:
			this->PC = this->FetchWord();
			break;
		case this->ROR_AC:
			this->EAX = this->ROR(this->EAX);
			break;
		case this->JSR:
			Address = this->FetchWord();
			this->PushPCToStack();
			this->PC = Address;
			this->cycles--;
			break;
		case this->RTS:
			Address = this->PopWordFromStack();
			this->PC = Address + 1;
			this->cycles -= 2;
			break;
		default:
			std::cout << "Invalid opcode at address 0x" << int_to_hex(this->PC - 1, 4) << ": 0x" << int_to_hex(Ins, 2) << std::endl;
			break;
		}
	}

	return cycles - this->cycles;
}