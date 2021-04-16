#include <Windows.h>

#include "emu.h"
#include "ram.h"
#include "cpu.h"
#include "display.h"
#include <thread>

using namespace emu;

const char g_szClassName[] = "myWindowClass";
RAM ram;
CPU cpu;

void StartCPU() {
	cpu.Boot();
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
	char bootfile[20];

	ram.data[0] = 1;
	cpu.Reset();

	LPWSTR* szArgList;
	int argCount;
	szArgList = CommandLineToArgvW((LPCWSTR)lpCmdLine, &argCount);
	strcpy_s(bootfile, (const char*)szArgList[0]);

	int error = ram.LoadBin(bootfile);

	if (error) {
		return error;
	}

	MSG Msg;
	
	error = InitilizeWindow(hInstance, nCmdShow, L"EMU", (LPCWSTR)g_szClassName);

	if (error) {
		return error;
	}

	std::thread cpu_thread(StartCPU);

	while (GetMessage(&Msg, NULL, 0, 0) > 0) {
		TranslateMessage(&Msg);
		DispatchMessage(&Msg);
	}

	char buffer[33];
	_itoa_s(cpu.Crash(), buffer, 33, 10);
	OutputDebugStringW("RIP: " + buffer);
	
	return Msg.wParam;
}
