#include "gpu.h"
#include "ram.h"

extern int WindowWidth;
extern int WindowHeight;
extern RAM ram;

void PaintWindow(HDC hdc) {
    int x, y, col;
    COLORREF color;

    for (int i = 0; i < (WindowWidth * WindowHeight); i++) {
        col = ram.data[i + 0xa0000];
        color = RGB(((col & 0b11100000) >> 5) * 32, ((col & 0b11100) >> 2) * 32, (col & 0b11) * 32);
        x = i % WindowWidth;
        y = floor(i / WindowWidth);
        SetPixel(hdc, x, y, color);
    }
}
