mov ah, 0x0e

mov al, [secret]
int 0x10                ; Shouldn't work. I think this is because we haven't used [org], or maybe because of segmentation?

mov bx, 0x7c0
mov ds, bx              ; Setup segmentation for data

; Everthing after this point will implicitly use the ds offset

mov al, [secret]        ; Works
int 0x10

mov al, [es:secret]     ; Use the es offset, apparently in programs you have to specifically say this
int 0x10

mov bx, 0x7c0           ; 0x7c0 refers to 0x7c00 >> 4 because of overlap
mov es, bx
; mov es, 0x7c0         ; Can only move raw values into general purpose registers, thats why you need to feed into bx, so then you can to register-to-register into es
mov al, [es:secret]
int 0x10                ; finally works

jmp $

secret:
    db "X"

times 510 - ($-$$) db 0
dw 0xaa55
