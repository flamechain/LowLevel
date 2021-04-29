#pragma once
#include "emu.h"

using namespace emu;

class RAM {
public:
	Byte data[0xa0001 + (640 * 480)]; // cant used vars in size because -std=c99 is not enabled
	int LoadBin(char filename[]);
	void Reset();
};
