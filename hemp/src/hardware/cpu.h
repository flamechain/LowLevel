#ifndef CPU_H
#define CPU_H

#include "rflags.h"
#include "types.h"

struct CPU {
    Qword RAX;
    Qword RBX;
    Qword RCX;
    Qword RDX;
    Qword RDI;
    Qword RSI;
    Qword RBP;
    Qword RSP;
    Qword R8;
    Qword R9;
    Qword R10;
    Qword R11;
    Qword R12;
    Qword R13;
    Qword R14;
    Qword R15;

    Qword CR0;
    Qword CR1;
    Qword CR2;
    Qword CR3;
    Qword CR4;
    Qword CR5;
    Qword CR6;
    Qword CR7;

    FExtend F800;
    FExtend F801;
    FExtend F802;
    FExtend F803;
    FExtend F804;
    FExtend F805;
    FExtend F806;
    FExtend F807;

    Qword RIP;

    union {
        Byte PS;
        struct RFLAGS FLAGS;
    };

    void (*Reset)(struct CPU*);
};

void Reset(struct CPU* self);

#endif
