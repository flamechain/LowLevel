#include "LCD.h"

void LCD::start() {
	this->init(L"LCD Display");
	this->Update(L"", 0);
}

LCD* window = nullptr;

LPCWSTR Text = L"";
int TextLen = 0;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam) {
	HDC hdc;
	switch (msg) {
	case WM_CREATE:
		window->onCreate();
		break;
	case WM_DESTROY:
		window->onDestroy();
		::PostQuitMessage(0);
		break;
	case WM_PAINT:
		PAINTSTRUCT ps;
		hdc = ::BeginPaint(hwnd, &ps);
		TextOut(hdc, 10, 10, Text, TextLen);
		::EndPaint(hwnd, &ps);
		break;
	default:

		return ::DefWindowProc(hwnd, msg, wparam, lparam);
	}

	return NULL;
}

void LCD::Update(LPCWSTR text, int text_len) {
	Text = text;
	TextLen = text_len;
}

bool LCD::init(LPCWSTR title) {
	WNDCLASSEX wc;
	wc.cbClsExtra = NULL;
	wc.cbSize = sizeof(WNDCLASSEX);
	wc.cbWndExtra = NULL;
	wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);
	wc.hInstance = NULL;
	wc.lpszClassName = L"LCD Display";
	wc.lpszMenuName = L"";
	wc.style = NULL;
	wc.lpfnWndProc = &WndProc;

	if (!::RegisterClassEx(&wc)) { return false; }
	if (!window) { window = this; }

	m_hwnd = ::CreateWindowEx(WS_EX_OVERLAPPEDWINDOW, L"LCD Display", L"LCD Display",
		WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 300, 70, NULL, NULL, NULL, NULL);

	if (!m_hwnd) { return false; }

	::ShowWindow(m_hwnd, SW_SHOW);
	::UpdateWindow(m_hwnd);

	m_isRun = true;

	return true;
}

bool LCD::release() {
	if (!::DestroyWindow(m_hwnd)) { return false; }
	return true;
}

void LCD::broadcast() {
	MSG msg;

	while (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE) > 0) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	window->onUpdate();

	Sleep(0);
}

bool LCD::isRun() {
	return m_isRun;
}

void LCD::onUpdate() {

}

void LCD::onDestroy() {
	m_isRun = false;
}

void LCD::onCreate() {}


