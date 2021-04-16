from CPU2 import CPU

cpu = CPU()
cpu.Data[0b00] = CPU.INS_ADD
cpu.Data[0b01] = 0b00
cpu.Data[0b10] = CPU.INS_STA
cpu.Data[0b11] = 0b11
cpu.Start()
print(cpu.A)