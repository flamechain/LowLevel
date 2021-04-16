#include "monitor.h"
#include "hardware/ram.h"
#include "hardware/cpu.h"
#include <stdio.h>
#include <string.h>

const char g_szClassName[] = "myWindowClass";
struct RAM ram;

/// WinMain Main, parameters handled by windows
/// @param  hInstance       Handle
/// @param  hPrevInstance   Previous handle
/// @param  lpCmdLine       Command line handle
/// @param  nCmdShow        Show command line
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Init for emulator
    char bootfile[20];

    ram.data[0] = 1;
    ram.LoadBin = LoadBin;

    struct CPU cpu;
    cpu.Reset = Reset;
    cpu.Reset(&cpu);

    LPWSTR *szArgList;
    int argCount;

    szArgList = CommandLineToArgvW((LPCWSTR)lpCmdLine, &argCount);
    strcpy(bootfile, (const char * restrict)szArgList[0]);

    if (ram.LoadBin(&ram, bootfile) == 1) {
        return 0;
    }

    MSG Msg = InitilizeWindow(hInstance, nCmdShow, "HEMP", g_szClassName);

    // Event loop
    while(GetMessage(&Msg, NULL, 0, 0) > 0) {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }

    return Msg.wParam;
}
