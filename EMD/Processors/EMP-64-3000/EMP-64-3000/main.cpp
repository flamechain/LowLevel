#include <Windows.h>

#include "emu.h"
#include "ram.h"
#include "cpu.h"
#include "display.h"
#include "gpu.h"
#include <thread>

using namespace emu;

const char g_szClassName[] = "myWindowClass";
RAM ram;
CPU cpu;
int WindowWidth = 640;
int WindowHeight = 480;

void StartCPU() {
	cpu.Boot();
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
	char bootfile[20];

	ram.Reset();
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
	HWND hwnd;
	
	error = InitilizeWindow(hInstance, nCmdShow, L"EMU", (LPCWSTR)g_szClassName, &hwnd);

	if (error) {
		return error;
	}

	std::thread cpu_thread(StartCPU);

	while (GetMessage(&Msg, NULL, 0, 0) > 0) {
		TranslateMessage(&Msg);
		DispatchMessage(&Msg);
	}

	cpu.Crash();
	cpu_thread.join();

	return Msg.wParam;
}
