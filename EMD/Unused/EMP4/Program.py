from CPU import CPU

cpu = CPU(25)

# Variables
n = 0xB
i = 0xC
Next = 0xD
First = 0xE
Second = 0xF

cpu.Data[n] = 13
cpu.Data[i] = 0
cpu.Data[Next] = 0
cpu.Data[First] = 0
cpu.Data[Second] = 1

# Instructions
cpu.Data[0x00] = CPU.INS_LDA
cpu.Data[0x01] = First
cpu.Data[0x02] = CPU.INS_LDB
cpu.Data[0x03] = Second
cpu.Data[0x04] = CPU.INS_ADD
cpu.Data[0x05] = Second
cpu.Data[0x06] = CPU.INS_STA
cpu.Data[0x07] = Next
cpu.Data[0x08] = CPU.INS_CMP
cpu.Data[0x09] = CPU.INS_CMP
cpu.Data[0x0A] = CPU.INS_JZS

cpu.Start()
