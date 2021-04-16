#pragma once
#include "emu.h"

using namespace emu;

class RAM {
public:
	Byte data[0xFFFF];
	int LoadBin(char filename[]);
};
