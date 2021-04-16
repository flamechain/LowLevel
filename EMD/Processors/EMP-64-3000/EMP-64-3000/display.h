#pragma once

#include "emu.h"
#include "gpu.h"
#include "ram.h"

using namespace emu;

void EventHandler(UINT eventid, int info);
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParma);
void EnterFullscreen(HWND hwnd);
int InitilizeWindow(HINSTANCE hInstance, int nCmdShow, LPCWSTR windowTitle, LPCWSTR className);
