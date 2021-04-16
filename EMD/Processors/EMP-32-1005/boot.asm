%include "screen.asm"

db "RW"

.code

    push "A"
    push 0
    push 0
    call print_char

    jmp $
