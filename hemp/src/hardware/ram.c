#include "ram.h"
#include <stdio.h>

int LoadBin(struct RAM* self, char filename[]) {
    const unsigned int filebuffer = 0xFFFF;
    char filecontents[filebuffer]; // using -std=c99 so this is actually allowed
    FILE *fp;

    fp = fopen(filename, "rb");

    if (fp == NULL) {
        printf("hemp: no valid input file\n");
        return 1;
    }

    printf("%s\n", fgets(filecontents, filebuffer, fp));
    fclose(fp);

    return 0;
}
