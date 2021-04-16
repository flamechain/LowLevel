#include "display.h"

bool initkeyup = true;

void EventHandler(UINT eventid, int info) {
	switch (eventid) {
    case WM_LBUTTONDOWN:
        OutputDebugStringW(L"LButtonDown\n");
        break;
    case WM_LBUTTONUP:
        OutputDebugStringW(L"LButtonUp\n");
        break;
    case WM_MBUTTONDOWN:
        OutputDebugStringW(L"MButtonDown\n");
        break;
    case WM_MBUTTONUP:
        OutputDebugStringW(L"MButtonUp\n");
        break;
    case WM_RBUTTONDOWN:
        OutputDebugStringW(L"RButtonDown\n");
        break;
    case WM_RBUTTONUP:
        OutputDebugStringW(L"RButtonUp\n");
        break;
    case WM_KEYDOWN:
        OutputDebugStringW(L"KeyDown: " + (wchar_t)info);
        break;
    case WM_KEYUP:
        if (initkeyup) {
            initkeyup = false;
            return;
        }
        OutputDebugStringW(L"KeyUp: " + (wchar_t)info);
        break;
    case WM_MOUSEWHEEL:
        if (info < 0) OutputDebugStringW(L"MouseWheelDown\n");
        else if (info > 0) OutputDebugStringW(L"MouseWheelUp\n");
        break;
    default:
        return;
	}
}

void EnterFullscreen(HWND hwnd) {
    DWord dwStyle = ::GetWindowLong(hwnd, GWL_STYLE);
    DWord dwRemove = WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX;
    DWord dwNewStyle = dwStyle & ~dwRemove;
    ::SetWindowLong(hwnd, GWL_STYLE, dwNewStyle);
    ::SetWindowPos(hwnd, NULL, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED);
    HDC hdc = ::GetWindowDC(NULL);
    ::SetWindowPos(hwnd, NULL, 0, 0, ::GetDeviceCaps(hdc, HORZRES), ::GetDeviceCaps(hdc, VERTRES), SWP_FRAMECHANGED);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    EventHandler(msg, (int)wParam);
    PAINTSTRUCT ps;
    HDC hdc;
    int err;

    switch (msg) {
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);
        err = PaintWindow(hdc, hwnd);
        EndPaint(hwnd, &ps);

        if (err) {
            return err;
        }

        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }

    return 0;
}

int InitilizeWindow(HINSTANCE hInstance, int nCmdShow, LPCWSTR windowTitle, LPCWSTR className) {
    WNDCLASSEX wc;
    HWND hwnd;

    int WindowWidth = 1920;
    int WindowHeight = 1080;

    // Window Properties
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    //wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.hbrBackground = CreateSolidBrush(RGB(0, 0, 0));
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

    return 0;
}
