#include "display.h"
#include "ram.h"
#include "gpu.h"
#include <thread>

bool initkeyup = true;
extern RAM ram;
extern int WindowWidth;
extern int WindowHeight;
int queue[10];

void EventHandler(UINT eventid, int info) {
    char buffer[15];
	switch (eventid) {
        // Removed mouse "driver" for simplicity
        case WM_KEYDOWN:
            _itoa_s(info, buffer, 10);
            OutputDebugStringW(L"\nKeyDown: " + (wchar_t)buffer);
            break;
        case WM_KEYUP:
            if (initkeyup) {
                initkeyup = false;
                return;
            }
            _itoa_s(info, buffer, 10);
            OutputDebugStringW(L"\nKeyUp: " + (wchar_t)buffer);
            break;
        case WM_MOUSEWHEEL:
            if (info < 0) OutputDebugStringW(L"MouseWheelDown\n");
            else if (info > 0) OutputDebugStringW(L"MouseWheelUp\n");
            break;
        default:
            return;
	}
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    std::thread event_thread(EventHandler, msg, (int)wParam);
    PAINTSTRUCT ps;
    HDC hdc;
    HDC hdesktop = GetDC(0);
    HDC memdc = CreateCompatibleDC(hdesktop);
    HBITMAP hbitmap = CreateCompatibleBitmap(hdesktop, WindowWidth, WindowHeight);
    SelectObject(memdc, hbitmap);

    switch (msg) {
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        case WM_PAINT:
            hdc = BeginPaint(hwnd, &ps);
            PaintWindow(memdc);
            BitBlt(hdc, 0, 0, WindowWidth, WindowHeight, memdc, 0, 0, SRCCOPY);
            EndPaint(hwnd, &ps);
            break;
        default:
            event_thread.join();
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }

    event_thread.join();
    return 0;
}

int InitilizeWindow(HINSTANCE hInstance, int nCmdShow, LPCWSTR windowTitle, LPCWSTR className, HWND* hwnd_) {
    WNDCLASSEX wc;
    HWND hwnd;

    // Window Properties
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = (LPCWSTR)className;
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc)) {
        MessageBox(NULL, L"Window Registration Failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return EMU_WINDOWREGISTRATIONFAILED;
    }

    // Create Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        className,
        windowTitle,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, WindowWidth, WindowHeight,
        NULL, NULL, hInstance, NULL);


    if (hwnd == NULL) {
        MessageBox(NULL, L"Window Creation Failed!", L"Error!", MB_ICONEXCLAMATION | MB_OK);
        return EMU_WINDOWCREATIONFAILED;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    hwnd_ = &hwnd;

    return 0;
}
