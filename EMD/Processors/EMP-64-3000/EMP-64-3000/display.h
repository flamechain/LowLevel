#pragma once
#include "emu.h"

using namespace emu;

void EventHandler(UINT eventid, int info);
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParma);
int InitilizeWindow(HINSTANCE hInstance, int nCmdShow, LPCWSTR windowTitle, LPCWSTR className, HWND* hwnd);
