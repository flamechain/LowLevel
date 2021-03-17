import CPU

cpu = CPU.CPU()
cpu.Data[0x0] = 0b0101_1000
cpu.Data[0x1] = 0b1101_0000
cpu.Data[0x2] = 0b0101_1001
cpu.Data[0x3] = 0b1101_0000
cpu.Execute(4)
