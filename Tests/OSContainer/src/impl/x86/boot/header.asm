section .multiboot_header
header_start:
    dd 0xe85250d6 ; multiboot2
    dd 0 ; Normal mode
    dd header_end - header_start ; length
    dd 0x100000000 - (0xe85250d6 + 0 + (header_end - header_start)) ; check-sum
    dw 0 ; end-tags
    dw 0
    dd 8
header_end:
