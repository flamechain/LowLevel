#include "cpu.h"

void Reset(struct CPU* self) {
    self->RAX = 0;
    self->RBX = 0;
    self->RCX = 0;
    self->RDX = 0;
    self->RDI = 0;
    self->RSI = 0;
    self->RBP = 0xA8001; // 0xFFFF below visual memory (0xb8000)
    self->RSP = self->RBP;
    self->R8 = 0;
    self->R9 = 0;
    self->R10 = 0;
    self->R11 = 0;
    self->R12 = 0;
    self->R13 = 0;
    self->R15 = 0;
    self->CR0 = 0;
    self->CR1 = 0;
    self->CR2 = 0;
    self->CR3 = 0;
    self->CR4 = 0;
    self->CR5 = 0;
    self->CR6 = 0;
    self->CR7 = 0;
    self->F800 = 0;
    self->F801 = 0;
    self->F802 = 0;
    self->F803 = 0;
    self->F804 = 0;
    self->F805 = 0;
    self->F806 = 0;
    self->F807 = 0;

    self->RIP = 0;

    self->FLAGS.CF = \
        self->FLAGS.ZF = \
        self->FLAGS.SF = \
        self->FLAGS.OF = \
        self->FLAGS.AF = \
        self->FLAGS.PF = \
        self->FLAGS.IF = \
        self->FLAGS.ID = 0;
}
