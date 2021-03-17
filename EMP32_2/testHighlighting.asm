include APackageThatDoesntExist

section .data
    ground: ascii "\n--------------------",0
    xPos: byte 10
    yPos: byte 8
    inputChar: byte ?

section .text

Function proc
    mov dh, yPos
    mov dl, xPos
    mov eax, "@"
    ret 0x00
Function endp

main proc
    ; draw ground at (0, 7)
    call Function
    ; mov edx, 0b00001000 << 8
    ; call Gotoxy
    mov edx, offset ground
    call WriteString

gameLoop:
    call ReadCha
    mov inputChar, eax
    cmp inputChar, "x"
    je exitGame

    cmp inputChar, "w"
    je moveUp
    cmp inputChar, "s"
    je moveDown
    cmp inputChar, "a"
    je moveLeft
    cmp inputChar, "d"
    je moveRight
    jmp gameLoop

moveUp:
    dec yPos
    call DrawPlayer
    jmp gameLoop

moveDown:
    inc yPos
    call DrawPlayer
    jmp gameLoop

moveLeft:
    dec xPos
    call DrawPlayer
    jmp gameLoop

moveRight:
    inc xPos
    call DrawPlayer
    jmp gameLoop

exitGame:
    ret 0x0

main endp

_start:
    call main
    ret
