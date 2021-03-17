; helloworld.asm

; eax: sys-call
; ebx: @param
; ecx: @param
; edx: @param

; 0x4 is __NR_write
; ebx is output
; ecx is message
; edx is message len

; 0x1 is __NR_exit
; ebx is return

; int (interupt) invokes the sys-call

; To create a string, use <varname>: db <string(s) seperated by comma>
; db is "define bytes"

; To get length of string, use <varname> equ $-<varname>
; equ is equals
; $- means length

global _start                        ; Tells that _start will be used

section .text:                       ; Instructions go under .text
_start:                              ; program counter goes here initially

    ; Print message

    mov eax, 0x4                     ; create write sys-call
    mov ebx, 1                       ; uses stdout as fd (file descriptor)
    mov ecx, message                 ; use message as buffer
    mov edx, message_len             ; use message_len as length (buffer bytes)
    int 0x80

    ; Exit program

    mov eax, 0x1                     ; create exit sys-call
    mov ebx, 0x0                     ; 0 return value means success
    int 0x80

section .data:                       ; Holds variables
    message: db "Hello, world!", 0xA ; Message
    message_len equ $-message        ; Message length
