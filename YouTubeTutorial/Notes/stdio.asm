section .data
    char: byte 0
    length: byte 0
    temp: word 0x1000
    format: word 0

section .text
printf proc
    mov char, 0
    mov length 0

_loop:
    mov char, [eax]
    cmp char, 0x0
    je _print
    inc eax
    inc length
    jmp _loop

_print:
    mov ecx, eax
    mov eax, 0x04
    mov ebx, 1
    mov edx, length
    int 0x80
    ret 0x0
printf endp


getchar proc
    mov eax, 0x03
    mov ebx, 1
    mov ecx, temp
    mov edx, 1
    int 0x80
    ret temp
getchar endp


putchar proc
    mov char, eax
    mov eax, 0x04
    mov ebx, 1
    mov ecx, char
    mov edx, 1
    int 0x80
    ret 0x0
putchar endp


scanf proc
    mov format, eax
    mov ecx, ebx
    mov eax, 0x03
    mov ebx, 1
    mov edx, 2048 ; 0x0800
    int 0x80
    mov length, 0

_loop:
    mov char, [ecx]
    cmp char, 0x0
    je _exit
    inc length
    inc ecx
    jmp _loop 

_exit:
    ret length
scanf endp
