#pragma once
#include <cmath>
#include <stdlib.h>
#include <iostream>

using Byte = unsigned char;
using Word = unsigned short;

class Memory {

private:
	std::string Hex(int value, int len, bool inc_0x = false);

public:
	Byte Data[65536]; // 16 ** 4

	void Reset();
	void ViewHex(int start_addr, int end_addr);
};
