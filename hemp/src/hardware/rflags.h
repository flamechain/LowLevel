#ifndef RFLAGS_H
#define RFLAGS_H

#include "types.h"

struct RFLAGS {
    Byte CF : 1;
    Byte ZF : 1;
    Byte SF : 1;
    Byte OF : 1;
    Byte AF : 1;
    Byte PF : 1;
    Byte IF : 1;
    Byte ID : 1;
    Byte Reserved;
    Word Res;
    Dword Unused;
};

#endif
