section .data
    curtime: dword 0
    oldtime: dword 0
    timer: byte 0

section .text
sleep proc
    mov timer, eax
    mov eax, 0x23 ;fTime
    mov ebx, 1
    mov ecx, oldtime
    int 0x80
    add oldtime, timer

_loop:
    mov eax, 0x23
    mov ebx, 1
    mov ecx, curtime
    int 0x80
    fcmp curtime, oldtime
    jne _loop
    jmp _exit

_exit:
    ret 0x0
sleep endp
