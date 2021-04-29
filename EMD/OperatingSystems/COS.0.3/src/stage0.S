.code16
.org 0

.text

.global _start
_start:
    cli

    /* segment setup */
    mov %cs, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %fs
    mov %ax, %gs
    mov %ax, %ss

    /* place stack pointer in middle of free memory area */
    movw $0x3000, %sp

    /* save drive number to read kernel later */
    mov %dl, drive_num

    sti

    /* should print OS TIME */
    movw $welcome_str, %si
    call print

    /* read kernel into memory at 0x10000 (segment 0x1000).
       kernel binary has been placed on the disk directly after the first sector
       reading $20 * num_sectors sectors after (value in %cx)
     */
    movw $20, %cx
    movb drive_num, %dl
    movw $disk_packet, %si
    movw $0x1000, segment
    movw $1, sector
sector_loop:
    movb $0x42, %ah
    int $0x13
    jc disk_error

    addw $64, sector
    addw $0x8000, offset
    jnc sector_same_segment

    /* increment segment, reset offset if on different segment */
    addw $0x1000, segment
    movw $0x0000, offset
sector_same_segment:
    /* decrements %cx and loops if nonzero */
    loop sector_loop

    /* video mode: 320x200 @ 16 colors */
    movb $0x00, %ah
    movb $0x13, %al
    int $0x10

    /* enable A20 line */
    cli

    /* read and save state */
    call enable_a20_wait0
    movb $0xD0, %al
    outb $0x64
    call enable_a20_wait1
    xorw %ax, %ax
    inb $0x60

    /* write new state with A20 bit set (0x2) */
    pushw %ax
    call enable_a20_wait0
    movb $0xD1, %al
    outb $0x64
    call enable_a20_wait0
    popw %ax
    orw $0x2, %ax
    outb $0x60

    /* enable PE flag */
    movl %cr0, %eax
    orl $0x1, %eax
    movl %eax, %cr0

    /* jmp to flush prefetch queue */
    jmp flush
flush:
    lidt idt
    lgdt gdtp

    movw $(gdt_data_segment - gdt_start), %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %es
    movw %ax, %fs
    movw %ax, %gs
    movw %ax, %ss
    movl $0x3000, %esp
    ljmp $0x8, $entry32

.code32
entry32:
    /* jump to kernel loaded at 0x10000 */
    movl $0x10000, %eax
    jmpl *%eax

_loop:
    jmp _loop

.code16
enable_a20_wait0:
    xorw %ax, %ax
    inb $0x64
    btw $1, %ax
    jc enable_a20_wait0
    ret

enable_a20_wait1:
    xorw %ax, %ax
    inb $0x64
    btw $0, %ax
    jnc enable_a20_wait1
    ret

disk_error:
    movw $disk_error_str, %si
    call print

/* prints string in %ds:si */
print:
    xorb %bh, %bh
    movb $0x0E, %ah

    lodsb

    /* NULL check */
    cmpb $0, %al
    je 1f

    /* print %al to screen */
    int $0x10
    jmp print

1:  ret

welcome_str:
    .asciz "OS TIME\n"
disk_error_str:
    .asciz "DISK ERROR\n"

/* SAVED DRIVE NUMBER TO READ FROM */
drive_num:
    .word 0x0000

/* INT 13H PACKET */
disk_packet:
    .byte 0x10
    .byte 0x00
num_sectors:
    .word 0x0040
offset:
    .word 0x0000
segment:
    .word 0x0000
sector:
    .quad 0x00000000

/* GDT */
.align 16
gdtp:
    .word gdt_end - gdt_start - 1
    /* .long (0x07C0 << 4) + gdt */
    .long gdt_start

.align 16
gdt_start:
gdt_null:
    .quad 0
gdt_code_segment:
    .word 0xffff
    .word 0x0000
    .byte 0x00
    .byte 0b10011010
    .byte 0b11001111
    .byte 0x00
gdt_data_segment:
    .word 0xffff
    .word 0x0000
    .byte 0x00
    .byte 0b10010010
    .byte 0b11001111
    .byte 0x00
gdt_end:

/* IDT */
idt:
    .word 0
    .long 0

.code32
.section .text.prologue
.section .text
.align 4

    movl $stack, %esp
    andl $-16, %esp
    movl $0xDEADBEEF, %eax
    pushl %esp
    pushl %eax
    cli
    call _main


.global idt_load
.type idt_load, @function
idt_load:
    mov 4(%esp), %eax
    lidt (%eax)
    ret

.macro ISR_NO_ERR index
    .global _isr\index
    _isr\index:
        cli
        push $0
        push $\index
        jmp isr_common
.endm

.macro ISR_ERR index
    .global _isr\index
    _isr\index:
        cli
        push $\index
        jmp isr_common
.endm

ISR_NO_ERR 0
ISR_NO_ERR 1
ISR_NO_ERR 2
ISR_NO_ERR 3
ISR_NO_ERR 4
ISR_NO_ERR 5
ISR_NO_ERR 6
ISR_NO_ERR 7
ISR_ERR 8
ISR_NO_ERR 9
ISR_ERR 10
ISR_ERR 11
ISR_ERR 12
ISR_ERR 13
ISR_ERR 14
ISR_NO_ERR 15
ISR_NO_ERR 16
ISR_NO_ERR 17
ISR_NO_ERR 18
ISR_NO_ERR 19
ISR_NO_ERR 20
ISR_NO_ERR 21
ISR_NO_ERR 22
ISR_NO_ERR 23
ISR_NO_ERR 24
ISR_NO_ERR 25
ISR_NO_ERR 26
ISR_NO_ERR 27
ISR_NO_ERR 28
ISR_NO_ERR 29
ISR_NO_ERR 30
ISR_NO_ERR 31
ISR_NO_ERR 32
ISR_NO_ERR 33
ISR_NO_ERR 34
ISR_NO_ERR 35
ISR_NO_ERR 36
ISR_NO_ERR 37
ISR_NO_ERR 38
ISR_NO_ERR 39
ISR_NO_ERR 40
ISR_NO_ERR 41
ISR_NO_ERR 42
ISR_NO_ERR 43
ISR_NO_ERR 44
ISR_NO_ERR 45
ISR_NO_ERR 46
ISR_NO_ERR 47

/* defined in isr.c */
.extern isr_handler
.type isr_handler, @function

isr_common:
    pusha
    push %ds
    push %es
    push %fs
    push %gs

    mov $0x10, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %fs
    mov %ax, %gs
    cld

    push %esp
    call isr_handler
    add $4, %esp

    pop %gs
    pop %fs
    pop %es
    pop %ds

    popa

    add $8, %esp
    iret

.section .data
.align 32
stack_begin:
    .fill 0x4000
stack:

/* MBR BOOT SIGNATURE */
.fill 510-($-$$), 0
.word 0xAA55
