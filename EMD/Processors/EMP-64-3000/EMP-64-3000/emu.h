#pragma once

#include <stdio.h>
#include <Windows.h>
#include <wingdi.h>

namespace emu {
	using Byte = unsigned char;
	using Word = unsigned short;
	using DWord = unsigned int;

	const int EMU_NOINPUTFILE = 1;
	const int EMU_INVALIDINPUTFILE = 2;
	const int EMU_WINDOWREGISTRATIONFAILED = 3;
	const int EMU_WINDOWCREATIONFAILED = 4;
	const int EMU_PAINTFAULT = 5;
}
