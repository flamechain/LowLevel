#include "monitor.h"
#include <stdio.h>
#include <stdbool.h>

bool initkeyup = true;

void EventHandler(UINT event_id, int info) {
    switch(event_id) {
        case WM_LBUTTONDOWN:
            printf("LButtonDown\n");
            break;
        case WM_LBUTTONUP:
            printf("LButtonUp\n");
            break;
        case WM_MBUTTONDOWN:
            printf("MButtonDown\n");
            break;
        case WM_MBUTTONUP:
            printf("MButtonUp\n");
            break;
        case WM_RBUTTONDOWN:
            printf("RButtonDown\n");
            break;
        case WM_RBUTTONUP:
            printf("RButtonUp\n");
            break;
        case WM_KEYDOWN:
            printf("KeyDown: %c\n", (wchar_t)info);
            break;
        case WM_KEYUP:
            if (initkeyup) {
                initkeyup = false;
                return;
            }

            printf("KeyUp: %c\n", (wchar_t)info);
            break;
        case WM_MOUSEWHEEL:
            if (info < 0) printf("MouseWheelDown\n");
            else if (info > 0) printf("MouseWheelUp\n");
            break;
        default:
            return;
    }
}

HWND CreateFullscreenWindow(HWND hwnd) {
    HMONITOR hmon = MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST);
    MONITORINFO mi = { sizeof(mi) };
    if (!GetMonitorInfo(hmon, &mi)) {
        return NULL;
    }
    return CreateWindow(TEXT("static"),
        TEXT("something interesting might go here"),
        WS_POPUP | WS_VISIBLE,
        mi.rcMonitor.left,
        mi.rcMonitor.top,
        mi.rcMonitor.right - mi.rcMonitor.left,
        mi.rcMonitor.bottom - mi.rcMonitor.top,
        hwnd, NULL, GetModuleHandle(NULL), 0);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    EventHandler(msg, (int)wParam);
    PAINTSTRUCT ps;
    HDC hdc;

    switch(msg) {
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        case WM_PAINT:
            hdc = BeginPaint(hwnd, &ps);
            PaintWindow(hdc, hwnd);
            EndPaint(hwnd, &ps);
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }

    return 0;
}

MSG InitilizeWindow(HINSTANCE hInstance, int nCmdShow, char windowTitle[], const char className[]) {
    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;

    char WindowTitle[] = "HEMP";
    int WindowWidth = 1920;
    int WindowHeight = 1080;

    // Window Properties
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = 0;
    wc.lpfnWndProc   = WndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = className;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);

    if(!RegisterClassEx(&wc)) {
        MessageBox(NULL, "Window Registration Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return Msg;
    }

    // Create Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        className,
        windowTitle,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, WindowWidth, WindowHeight,
        NULL, NULL, hInstance, NULL);

    // Widgets

    // HWND fullscreen = CreateFullscreenWindow(hwnd);

    if(hwnd == NULL) {
        MessageBox(NULL, "Window Creation Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return Msg;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    return Msg;
}