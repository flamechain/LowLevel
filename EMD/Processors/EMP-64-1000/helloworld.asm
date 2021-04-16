; TODO: make sure to fix assembler to accept all filenames
.bss
stack_bottom:
    stack resb 4096
stack_top:

.code

check_multiboot proc
    cmp eax, 0x36d76289
    jne no_multiboot
    ret
check_multiboot endp

no_multiboot:
    mov al, "M"
    jmp error

error:
    mov dword [0xb8000], 0x4f454f52
    mov dword [0xb8004], 0x4f524f3a
    mov dword [0xb8008], 0x4f204f20
    mov byte [0xb800a], al
    hlt

main proc
    mov esp, stack_top

    call check_multiboot
    call check_cpuid
    call check_long_mode

    ret
main endp
end
