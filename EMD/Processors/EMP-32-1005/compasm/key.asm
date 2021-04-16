.code
    push "A"        ; Char
    push 0          ; X
    push 1          ; Y
    call print_char
    hlt

print_char:         ; void print_char(char Char, int X, int Y);
    pop r8          ; ret address
    pop rcx         ; Y
    pop rbx         ; X
    pop rax         ; Char

    cmp rax, "A"    ; switch(Char)
    je let_upperA

let_upperA:
    mov [0xb8000 + rbx + (1920*rcx)], 0
    mov [0xb8000 + rbx + (1920*rcx)], 0
