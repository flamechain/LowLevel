section .text
_start:
    mov 0xb8000, 0x2f4b2f4f
    hlt

section .data
vars:
    message: .ascii "hello, world!"
    message_len: len message
    other_var: 0x01 + message_len *2 + 0b111
