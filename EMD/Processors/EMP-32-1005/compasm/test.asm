.include "C:\empasm\libs\stdio.inc"

.globl Main

.bss
    a resb 1
    b resb 1
    d resd 1
    c resd 1
    e resw 1
    f resw 1
    g resq 1
    h resq 1
    i resd 5
    j resb 6

.data
    i db 1, 2, 3, 4, 5
    j db "Hello", 0

.text
Main:
    push j
    call printf
    hlt
