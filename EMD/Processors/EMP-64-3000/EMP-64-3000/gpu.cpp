#include "gpu.h"

extern RAM ram;

int PaintWindow(HDC hdc, HWND hwnd) {
	COLORREF white = RGB(255, 255, 255);
	RECT rect;
	rect.left = 0;
	rect.top = 0;
	rect.right = 200;
	rect.bottom = 200;
	HBRUSH hbr = CreateSolidBrush(white);
	//GetClientRect(hwnd, &rect);
	//DrawText(hdc, L"Hello, world!", -1, &rect, DT_LEFT | DT_TOP);
	if (!Rectangle(hdc, 0, 0, 200, 200)) {
		return EMU_PAINTFAULT;
	}
	if (!FillRect(hdc, &rect, hbr)) {
		return EMU_PAINTFAULT;
	}
}
