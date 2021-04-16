#pragma once

#include <stdio.h>
#include <Windows.h>
#include <wingdi.h>

namespace emu {
	using Byte = unsigned char;
	using Word = unsigned short;
	using DWord = unsigned int;
	using QWord = unsigned long;
	using DQWord = unsigned long long;
	using FSingle = float; // real
	using FDouble = double;
	using FExtend = double long;

	const int EMU_NOINPUTFILE = 1;
	const int EMU_INVALIDINPUTFILE = 2;
	const int EMU_WINDOWREGISTRATIONFAILED = 3;
	const int EMU_WINDOWCREATIONFAILED = 4;
	const int EMU_PAINTFAULT = 5;
}
