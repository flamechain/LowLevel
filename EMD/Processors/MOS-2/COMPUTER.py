import sys

here = '\\'.join(__file__.split('\\')[:-1])
bins = here + '\\src\\bin\\'
scripts = here + '\\src\\scripts\\'

sys.path.append(scripts)
sys.path.append(scripts + 'utils\\')

import CPU
import BIOS
import GPU
import pygame
import threading

pygame.init()
boot_bin, eprom_bin = BIOS.bios()
window = pygame.display.set_mode((1910, 1020), pygame.RESIZABLE)
run = True
clock = pygame.time.Clock()
t = threading.Thread(target=CPU.CPU, args=['011101 00000000000000000000000000', boot_bin, eprom_bin])
t.start()
gpu = GPU.GPU(window)

while run:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            with open(bins + 'Registers.bin', 'r') as f:
                copy = f.readlines()
            flags = [i for i in copy[0].replace(' ', '').strip('\n')]
            flags[1] = '1'
            flags = ' '.join(flags) + '\n'
            copy[0] = flags
            with open(bins + 'Registers.bin', 'w') as f:
                f.write(''.join(copy))

    clock.tick(29)
    gpu.update()
    pygame.display.update()

pygame.quit()
