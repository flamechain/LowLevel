#ifndef GPU_H
#define GPU_H

#include "cpu.h"
#include "ram.h"
#include <windows.h>

/// PaintWindow: Handles GPU painting
/// @param  hdc     Paint handle (Handle-DC)
/// @param  hwnd    Window handle (Handle-WiNDow)
void PaintWindow(HDC hdc, HWND hwnd);

/// RectDraw: Draws a rectangle
/// @param  hdc     Paint handle
/// @param  left    xLeft
/// @param  right   xRight
/// @param  top     yTop
/// @param  bottom  yBottom
void RectDraw(HDC hdc, int left, int right, int top, int bottom);

#endif
