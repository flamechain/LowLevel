#ifndef RAM_H
#define RAM_H

struct RAM {
    char data[0xFFFF]; // Max: 0x1f96fc, 2070268
    int (*LoadBin)(struct RAM* self, char filename[]);
};

int LoadBin(struct RAM* self, char filename[]);

#endif
