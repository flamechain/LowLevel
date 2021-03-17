.text:
_start:
    mov eax, write_syscall
    mov ebx, stdout
    mov ecx, *message
    mov edx, message_len
    int call_sys

    mov eax, exit_syscall
    mov ebx, return
    int call_sys

.data:
    message: .ascii "Hello, world!"
    message_len: equ $-message
    write_syscall: 0x1
    exit_syscall: 0x0
    call_sys: 0x1
    stdout: 0x1
    return: 0x0
