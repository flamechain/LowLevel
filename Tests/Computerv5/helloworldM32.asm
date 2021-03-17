.section .text:
_start:
    mov eax, 0x1
    mov ebx, 0x1
    mov ecx, *message
    mov edx, *message_len
    int 0x1

    mov eax, 0x0
    mov ebx, 0x0
    int 0x1

.section .data:
    message: .ascii "Hello, world!"
    message_len: equ $-message
