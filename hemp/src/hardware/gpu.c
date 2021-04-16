#include "gpu.h"
#include <stdio.h>

extern struct RAM ram;

void RectDraw(HDC hdc, int left, int right, int top, int bottom) {
    RECT rect;
    rect.bottom = bottom;
    rect.top = top;
    rect.left = left;
    rect.right = right;
    // DrawFocusRect(hdc, &rect);
    HBRUSH hbr = (HBRUSH)RGB(255,0,0);
    FillRect(hdc, &rect, hbr);
}

void PaintWindow(HDC hdc, HWND hwnd) {
    RECT rect;
    GetClientRect(hwnd, &rect);
    HBRUSH hbr = (HBRUSH)0xFF0000;
    FillRect(hdc, &rect, hbr);
    // DrawText(hdc, (LPCSTR)"abcdefghijklmnopqrstuvwxyz", -1, &rect, DT_LEFT | DT_TOP);
    // RectDraw(hdc, 10, 200, 30, 300);
}
