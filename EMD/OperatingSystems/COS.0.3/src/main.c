#include "util.h"
#include "screen.h"
#include "idt.h"
#include "isr.h"
#include "irq.h"
#include "font.h"
#include "system.h"

#define FPS 30

void _main(u32 magic) {
    idt_init();
    isr_init();
    irq_init();
    screen_init();
}
