mov eax, eax
; 89 c0 -> 11 000 000
mov ecx, eax
; 89 c1 -> 11 000 001
mov edx, eax
; 89 c2 -> 11 000 010
mov ebx, eax
; 89 c3 -> 11 000 011
mov esp, eax
; 89 c4 -> 11 000 100
mov ebp, eax
; 89 c5 -> 11 000 101
mov esi, eax
; 89 c6 -> 11 000 110
mov edi, eax
; 89 c7 -> 11 000 111

mov eax, eax
; 89 c0 -> 11 000 000
mov eax, ecx
; 89 c8 -> 11 001 000
mov eax, edx
; 89 d0 -> 11 010 000
mov eax, ebx
; 89 d8 -> 11 011 000

; 89 for RegReg -> 1000 1001
; b8 for RegIm ->  1011 1000
