'''
Computer Emulator v3

This is a project that contains everything from a CPU, to an ASM language.

File contains the connections between parts, and the housing for the virtual memory.
'''

import time
import threading

import pygame

from Memory import VirtualMemory
from CPU import CPU
from LCD import LCD

with open('helloworld.bin', 'r') as f:
    program = f.read()

cpu = CPU()
cpu.LoadProgram(program)

pygame.init()
window = pygame.display.set_mode((300, 70))
display = LCD(window, pygame)

def keystrokes(key):
    if key == pygame.K_a:
        print('a pressed')

def main(display):
    '''Runs program with LCD'''
    time.sleep(1/10)
    odd = False

    run = True
    while run:
        cpu.Execute(1)
        if odd:
            output = (cpu.out[0] << 8) | (cpu.out[1])
            display.input = output
            display.clock = 1
            odd = False
        else:
            odd = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                keystrokes(event.key)
        
        pygame.display.update()
    
    display.run = False
    pygame.quit()

t = threading.Thread(target=display.Start, args=[pygame])
t.start()
main(display)
