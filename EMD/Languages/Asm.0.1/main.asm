.bss
    path resb 50
.data
    flt dq 0x1028 ; sudo code for a file location table
.code

ParseArgs proc
    mov r8, rax
    mov rcx, rax
    xor rax, rax
loop:
    inc rax
    mov rdx, [rcx]
    cmp rdx, 0
    je end
    inc rcx
    jmp loop
end:
    ret
ParseArgs endp

Main proc
    call ParseArgs
    cmp rax, 0
    je error1
    cmp rax, 1
    mov path, r8
    jg error2

error1:
    mov rax, 1
    ret
error2:
    mov rax, 2
    ret
Main endp

CmpString proc ; how file file????
CmpString endp
