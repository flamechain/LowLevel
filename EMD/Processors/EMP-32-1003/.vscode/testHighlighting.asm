include stdio

.globl _start

.const Var1, 1000
.const Var2, 0x1
.const Var3, 0b1

section .data
    msg: ascii "Hello, world!",0
    msg_len: len msg
    Var4: byte 1
    Var5: word 0x1
    Var6: dword 0b1
    Var7: tword 0b11
    Var8: qword 0xF

section .bss
    Label1: db 100

section .text

main proc
    jmp Label1
    ret
main endp

Label1:
    mov %eax, %ebx
    .del Label1

_start:
    call main
    call AllIns
    ret

AllIns proc
    abs
    adc
    add
    and
    bswap
    busy
    call
    chs
    clc
    cli
    clo
    cls
    clz
    cmp
    cos
    dec
    div
    dvc
    eflip
    fabs
    fadd
    fchs
    fcmp
    fdiv
    fint
    fld1
    fldpi
    fldz
    fmul
    fscale
    fsqrt
    fsub
    ftst
    hlt
    iadd
    idle
    idiv
    imul
    in
    inc
    int
    isub
    jc
    je
    jg
    jge
    jl
    jle
    jmp
    jmpahd
    jnc
    jne
    jno
    jns
    jnz
    jo
    js
    jz
    ldao
    lock
    loop
    mlc
    mov
    mul
    not
    nop
    out
    or
    pop
    pope
    popf
    push
    pushe
    pushf
    ret
    rol
    ror
    sal
    sar
    sbc
    scale
    shl
    shr
    sin
    sqrt
    stao
    stc
    sti
    sto
    sts
    stz
    sub
    tan
    tst
    wait
    xchg
    xchge
    xchgw
    xor
AllIns endp

; comment
 ; comment
    ;comment
