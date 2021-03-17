; section .data                       ; variable section
;     message: .ascii "Hello, world!" ; string
;     msg_len: len message            ; length of string

; section .code                       ; procedures

; main PROC                           ; main
;     mov eax, %ebp                   ; mov eax, value of ebp
;     ret                             ; return, sets edi with return (default 0)
; main END

; section .text                       ; non-func instructions

; _start:                             ; OS jumps here, auto global
;     call main                       ; invokes function
;     jmp exit                        ; jump to label

; exit:                               ; exit label
;     ret                             ; return to OS

section .text
_start:
    mov eax, 0
    hlt
