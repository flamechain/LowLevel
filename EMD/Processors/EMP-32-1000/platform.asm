INCLUDE EMPIrvine

section .data
    ground: .ascii "-------------------------",0

section .code

main PROC
    mov edx, OFFSET ground
    call WriteString
    call ReadChar
main ENDP

section .text
_start:
    call main
    hlt
