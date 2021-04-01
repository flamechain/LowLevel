mov ah, 0x0e            ; tty mode

mov bp, 0x8000          ; Base of the stack, where the stack starts and grows down from
mov sp, bp              ; Updating the stack pointer to the stack base, "base pointer"

push "A"
push "B"
push "C"

mov al, [0x7ffe]        ; Where the stack is to show it growing down. Should print "C"
int 0x10

mov al, [0x8000]        ; Apparently you can only access the top of the stack, so only 0x7ffe will contain the stack value
int 0x10                ; Otherwise this would print "A"

pop bx                  ; I think you have to pop into a 16 bit register
mov al, bl              ; So then we move bl into al
int 0x10                ; "C", because its first in last out

pop bx
mov al, bl
int 0x10                ; "B"

pop bx
mov al, bl
int 0x10                ; "A"

mov al, [0x8000]        ; Now the data has been popped so we can look at the top, but it will be garbage because we didn't put anything there purposly
int 0x10

; push "D"                ; Will be an error because you can't pop into an 8-bit register (tested)
; pop al
; int 0x10



jmp $                   ; Jumps to the current address, which is the address at the start of the jmp instruction
                        ; Meaning it will jump back to the beginning of the jmp instruction


times 510 - ($-$$) db 0 ; Loops 510 times placing a 0x00 byte,
dw 0xaa55               ;A magic number to indicate that this can boot
