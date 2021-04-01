.data
    msg db "Hello, world!\n"
    msg_len equ $ - msg

.code
main proc
    mov eax, 0x4
    mov ebx, 1
    mov ecx, msg
    mov edx, [msg_len]
    syscall ; int 0x80

    ret
main endp
end
