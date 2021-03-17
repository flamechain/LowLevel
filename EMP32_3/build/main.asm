include stdio
section .data
    msg: ascii "Hello, world!"
    msg_len: len msg
section .text
main proc
    mov eax, msg
    mov ebx, msg_len
    call printf
    ret 0
main endp
_start:
    call main
    ret