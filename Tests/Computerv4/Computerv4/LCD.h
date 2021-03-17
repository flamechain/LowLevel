#pragma once
#include <Windows.h>
#include <string>

class LCD {
private:
	bool init(LPCWSTR title);
	bool release();
	void Update(LPCWSTR text, int text_len);
	void onUpdate();
	bool m_isRun;

public:
	void broadcast();
	void start();
	bool isRun();
	void onCreate();
	void onDestroy();
	void Execute();
	int cycles;

	HWND m_hwnd;
};
