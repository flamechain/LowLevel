.data
    a equ 7
    b equ 3
    z equ 0
    h1 equ -1
    h2 equ 0

.text
    : b, b          ; MOV b, a
    : z, a
    : b, z
    : z, z
    : h1, h2, $     ; HLT

