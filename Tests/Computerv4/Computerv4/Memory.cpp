#include "Memory.h"
#include "definitions.h"

void Memory::Reset() {
	for (int i = 0; i < 65536; i++) {
		this->Data[i] = 0x00;
	}
}

std::string Memory::Hex(int value, int len, bool inc_0x) {
	std::string hexvalue = "";
	hexvalue = int_to_hex(value, len);
	if (inc_0x) { hexvalue = "0x" + hexvalue; }

	return hexvalue;
}

void Memory::ViewHex(int start_addr, int end_addr) {
	system("Color 08");
	std::cout << "       00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F\n";

	float bysxtn = start_addr / 16;
	start_addr = floor(bysxtn) * 16;

	for (int i = start_addr; i < end_addr; i += 16) {
		system("Color 08");
		std::cout << this->Hex(i, 4, true);

		for (int j = i; j < (i + 16); j++) {
			std::string toprint = this->Hex(this->Data[j], 2);

			if (toprint == "cc") { system("Color 08"); }
			else { system("Color 07"); }

			std::cout << ' ' << toprint;
		}

		std::cout << '\n';
	}
}
