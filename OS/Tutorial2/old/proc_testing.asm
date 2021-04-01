[org 0x7c00]            ; Origin of the bootsector

my_program:
    push HELLO              ; Convention of function parameters
    call printf             ; Call printf, defined in "stdio.asm"

    push GOODBYE
    call printf
end_progrm:


jmp $                   ; Jumps to the current address, which is the address at the start of the jmp instruction
                        ; Meaning it will jump back to the beginning of the jmp instruction

%include "stdio.asm"   ; After code

; .data
HELLO:
    db "Hello, world!", 0x0a, 0

GOODBYE:
    db "Goodbye", 0x0a, 0


times 510 - ($-$$) db 0 ; Loops 510 times placing a 0x00 byte,
dw 0xaa55               ;A magic number to indicate that this can boot
