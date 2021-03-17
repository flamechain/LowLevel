section .text
printf proc
    mov ecx, ebx
    mov ebx, eax
    mov eax, 0
    mov edx, 0
    int 1
    ret
printf endp
