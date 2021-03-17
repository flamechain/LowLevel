section .text
_start:
    mov eax, message
    mov ebx, msg_len
    hlt

section .data
    message: .ascii "Hello, world!\n"
    msg_len: len message
