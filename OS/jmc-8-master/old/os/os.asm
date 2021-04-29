; JMC-8 kernel/os

.org 0

; @TODO: Move this block
; Things that need testing in the circuit diagram
.block
NEED TESTING:
PUSH REG
POP REG
JNZ IMM
JNZ REG
WRITING DIRECTLY TO PC VIA MEMORY
.endblock

; OS call vector table
; Do not update without also changing os_include.inc
; Each successive call vector is 5 bytes in size
jmp os_main     ; 0x0000
jmp some_call   ; 0x0005
jmp other_call  ; 0x000A
; ...

os_main:
    jmp $
