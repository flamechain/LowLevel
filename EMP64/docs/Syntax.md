# EMP64 Assembly Syntax Differences

Variables are stored by address, so the syntax for getting values is opposite.

```asm
.data
    MyValue dq 1
.code
main proc
    mov rax, MyValue   ; Address where MyValue is located
    mov rax, [MyValue] ; Value at the address (square brackets mean at address) of MyValue
    ; Variables are basically labels, and the defining bytes are just normal defining byte statements
    ret
main endp
end
```

This is the same as

```asm
.data
MyValue:
    dq 1
.code
main proc
    mov rax, MyValue
    mov rax, [MyValue]
    ret
main endp
end
```

This works out because the assembler knows you defined 8 bytes because your moving into rax, not eax, ax, or al.
