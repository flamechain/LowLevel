; helloworld.asm

loop:
    *=$1000               ; start address
    ldx #$00              ; counter
    lda message, x        ; pointer to message letter plus X, acts at <for i in message:>
    sta $0400, x          ; screen position plus X, so each letter has an offset from the corner
    inx                   ; increments X as <i>
    cpx #$0C              ; quits if X excedes message length
    bne loop
    rts

message
    .text "Hello, world!" ; pointer to auto-created message
