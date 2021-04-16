print_char:                     ; void print_char(char let, int x, int y);
    pop edx
    pop al                      ; char let
    pop ebx                     ; int x
    pop ecx                     ; int y
    push edx

    mov edi, 0xb8000
    mul ebx, 2
    add edi, ebx
    mul ecx, 160
    add edi, ecx
    sal ax, 8
    or ax, 0xf
    mov [edi], ax

    xor eax, eax
    ret

clear_screen:                   ; void clear_screen();
    mov ecx, 0xb8000

_c_loop:
    cmp ecx, 0xb9f40            ;  0xb8000 + (80*50*2)
    je _c_exit

    mov [ecx], 0
    inc ecx

    jmp _c_loop

_c_exit:
    xor eax, eax
    ret

scroll_down:                    ; void scroll_down(int lines);
    pop edx
    pop cx                      ; int lines
    push edx

    mov edi, 0xb8000            ; dest
    mov esi, 0xb8000            ; src

    mul cx, 25                  ; screen width
    mul cx, 2                   ; each character takes 2 bytes, format, and character
    add esi, cx

_s_loop:
    cmp edi, 0xb9f40            ;  0xb8000 + (80*50*2)
    je _s_exit

    cmp esi, 0xb9f40
    je _s_special

    mov [edi], [esi]
    inc edi
    inc esi

    jmp _s_loop

_s_special:
    mov [edi], 0
    inc edi

    jmp _s_loop

_s_exit:
    xor eax, eax
    ret
