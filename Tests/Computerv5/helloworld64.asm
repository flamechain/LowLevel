; helloworld.asm

; uses . at the beginning of sections and globals, not to mistake with variables

.global _start

.section .text:
_start:

    mov x8, #64                       ; write sys-call
    mov x0, #1
    ldr x1, =message                  ; pointer (address) of message, ldr is a shortcut for mov that is more efficent
    ldr x2, =message_len              ; == mov x2, message_len
    svc 0

    ; Exit program

    mov x8, #0x5d                     ; Puts #0x5d into register code x8, #0x5d is the exit sys-call
    mov x0, #0x41                     ; @param for exit, error code. I dont know what this error code is
    svc 0                             ; system service 0, gets kernels help (sys-call)


.section .data:
    message: .ascii "Hello, world!\n" ; You can use escaped chars instead of char codes. You use .ascii instead of db
    message_len: equ $ - message