#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "CPU.h"
#include "LCD.h"

void ReadLine() {
	char empty[2];
	fgets(empty, 2, stdin);
}

int main() {
	LCD lcd;
	lcd.start();

	while (lcd.isRun()) {
		lcd.broadcast();
	}

	return 0;
}
