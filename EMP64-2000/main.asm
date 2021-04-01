.bss
idt:
    resb 0x400

.text
main:
    mov esp, stack_top

    call check_multiboot
    call check_cpuid
    call check_long_mode

    ; print 'OK'
    mov dword [0xb8000], 0x2f4f2f4b
    hlt

check_multiboot:
    cmp eax, 0x36d76289
    jne no_multiboot
    ret

.bss
stack_bottom:
    resb 4096 * 4
stack_top:

    resb 0xb4000
