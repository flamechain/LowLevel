# Info

6502 CPU Emulator

___

- Little Endian: stores least significent byte first. 0x40 -> 0x80 = 0x8040
- 0xFFFC and 0xFFFD contain a word of the start address; Execution doesn't start at 0xFFFC
- ADC may be incorrect, very sloppy
