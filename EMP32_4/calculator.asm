include stdio

.globl _start

section .data
    read: byte 3
    write: byte 4
    stdout: byte 1
    stdin: byte 1
    syscall: byte 128
    msg1: ascii "Enter number 1: "
    msg2: ascii "Enter number 2: "
    msg3: ascii "[1] Add\n[2] Sub\n[3] Mul\n[4] Div\nEnter Operation: "
    num1: word 0x100
    num2: word 0x109
    op: word 0x10A

section .text

main proc
    mov eax, msg1
    call printf

    mov eax, "s"
    mov ebx, num1
    call scanf

    mov eax, msg2
    call printf

    mov eax, "s"
    mov ebx, num2
    call scanf

    mov eax, msg3
    call printf

    mov eax, "s"
    mov ebx, op
    call scanf

main endp

convert proc
convert endp

_start:
    call main
    ret
