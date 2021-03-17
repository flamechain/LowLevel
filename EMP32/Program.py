import CPU

cpu = CPU.CPU()
cpu.LoadProgram('plt.bin')
cpu.Bootup()
print(cpu.EDI)
