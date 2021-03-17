section .data
    oldtime: dword ?
    newtime: dword ?
    msg: ascii "1 Second Done"

section .text
_start:
    mov eax, 0x0D      ; Sys_Time
    mov ebx, oldtime ; time_t *tloc
    int 0x80           ; Syscall
    inc oldtime

_loop:
    mov eax, 0x0D
    mov evx, newtime
    int 0x80

    cmp oldtime, newtime
    jne _loop

    mov eax, 0x04 ; Sys_Write
    mov ebx, 1
    mov ecx, msg
    mov edx, 0x0
    int 0x80

    mov eax, 0x01 ; Sys_Exit
    mov ebx, 0x0
    int 0x80
