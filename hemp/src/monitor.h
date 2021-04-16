#ifndef MONITOR_H
#define MONITOR_H
#include <locale.h>
#include <windows.h>
#include "hardware/gpu.h"
#include "hardware/ram.h"

/// EventHandler: Handles events for CPU
/// @param  eventid ID for events
/// @param  info    WPARAM extra info
void EventHandler(UINT eventid, int info);

/// WndProc: WinMain event handler
/// @param  hwnd    Handle, main window
/// @param  msg     Event ID
/// @param  wParam  Extra info
/// @param  lParam  Extra info
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

/// CreateFullscreenWindow: Creates a fullscreen window
/// @param  hwnd    Handle
HWND CreateFullscreenWindow(HWND hwnd);

/// InitilizeWindow: Creates window and handles everything but the message loop
/// @param  hInstance       Handle
/// @param  hPrevInstance   Previous handle
/// @param  lpCmdLine       Command line handle
/// @param  nCmdShow        Show command line
MSG InitilizeWindow(HINSTANCE hInstance, int nCmdShow, char windowTitle[], const char className[]);

#endif
