#include "ram.h"

int RAM::LoadBin(char filename[]) {
	const unsigned int filebuffer = 0xFFF;
	char filecontents[filebuffer];
	FILE* fp;
	errno_t err;

	err = fopen_s(&fp, filename, "rb");

	if (fp == NULL || err) {
		return EMU_INVALIDINPUTFILE;
	}

	OutputDebugStringW((LPCWSTR)fgets(filecontents, filebuffer, fp));
	fclose(fp);

	return 0;
}
