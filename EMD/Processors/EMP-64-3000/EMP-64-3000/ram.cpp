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

	fgets(filecontents, filebuffer, fp);
	fclose(fp);

	for (int i = 0; i < sizeof filecontents; i++) {
		this->data[i] = filecontents[i];
	}

	return 0;
}

void RAM::Reset() {
	for (int i = 0; i < sizeof this->data; i++) {
		this->data[i] = 0;
	}
}
