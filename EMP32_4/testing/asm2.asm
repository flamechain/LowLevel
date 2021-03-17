; This is the inital assembler version, manualy compiled into machine code.
; This will be bootstrapped later to upgrade itself.
;
; The test for this program is its ability to assemble itself.
; I will assemble it manually, then run it on itself.
; Then run the assemblers assembled assembler on stdio.asm to test

.globl _start

section .data
    .const buffer: dword 0x10000
    ; *[filename], *[file], *[err_msg], and constants
    filename: ascii "", 0 .buf 20
    file: dword 0xF000F
    err_msg: ascii "", 0 .buf 60
    newfilename: ascii "", 0 .buf 20
    counter: dword 0x0
    counter2: byte 0x0
    char: byte 0x0
    result: ascii "", 0 .buf buffer
    result_counter: dword result

    .const sys_exit: byte 0x01
    .const sys_read: byte 0x03
    .const sys_write: byte 0x04
    .const sys_open: byte 0x05
    .const sys_close: byte 0x06
    .const stdout: byte 0x01
    .const stdin: byte 0x01
    needed_instructions: db "jmp", "mov", "ret", "int", "cmp", "je", "jne", "call"

section .text

ParseArgs proc
    ; Parses arguments, currently just [filename]
    mov eax, sys_open
    mov ebx, filename
    mov ecx, [buffer]
    int 0x80
    ret eax
ParseArgs endp

GetArgs proc
    ; Gets arguments from user using stdin, cant use command line because
    ; im not directly invoking this program, im calling the CPU which will
    ; have this loaded.
    mov eax, sys_read
    mov ebx, stdin
    mov ecx, filename
    mov edx, 20
    int 0x80
    ret 0x0
GetArgs endp

AssemblePassOne proc
    mov result_counter, "a"
    inc result_counter
    ret 0x0
AssemblePassOne endp

AssemblePassTwo proc
    mov result_counter, "b"
    inc result_counter
    ret 0x0
AssemblePassTwo endp

FinishFile proc
    mov eax, sys_close
    mov ebx, filename
    int 0x80

    mov counter, newfilename
_ff_loop:
    mov char, [filename]
    cmp char, "."
    je _ff_finish
    mov counter, char
    inc counter
    jmp _ff_loop
_ff_finish:
    mov counter, "."
    inc counter
    mov counter, "b"
    inc counter
    mov counter, "i"
    inc counter
    mov counter, "n"

    mov eax, sys_create
    mov ebx, newfilename
    int 0x80

    mov eax, sys_open
    mov ebx, newfilename
    mov ecx, buffer
    int 0x80

    mov counter, result
    mov counter2, 0
    mov char, counter
_ff_writing:
    mov file, char
    cmp counter2, buffer
    je _ff_done
    inc counter2
    inc counter
    mov char, counter

_ff_done:
    ret 0x0
FinishFile endp

_start:
    ; Gets [filename] input
    ; [fileout] is [filename].bin ( .o later when portability is implemented)
    call GetArgs
    call ParseArgs
    cmp eax, 0x0
    jne _error
    call AssemblePassOne
    cmp eax, 0x0
    jne _error
    call AssemblePassTwo
    cmp eax, 0x0
    jne _error
    call FinishFile
    cmp eax, 0x0
    jne _error
    mov ebx, 0x0
    jmp _exit

_error:
    ; Write to screen [err_msg], and calls [_exit] with error code 1
    mov eax, sys_write
    mov ebx, stdout
    mov ecx, err_msg:
    mov ebx, 60
    int 0x80
    mov ebx, 0x01
    jmp _exit

_exit:
    ; Exits using the Exit syscall
    mov eax, sys_exit
    int 0x80 ; ret ebx
