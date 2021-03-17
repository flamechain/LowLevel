INCLUDE user32

section .data
    msg: .ascii "My Window", 0
    text: .ascii "Hello, world!", 0

section .text
_start:
    mov eax, 0
    mov ebx, msg
    mov ecx, text
    mov edx, 0
    call Windows
    hlt
