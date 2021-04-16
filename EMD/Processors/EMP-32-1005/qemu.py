import sys

# sys.argv[0] is always the current filename, so it can be stripped
args = sys.argv[1:]

# Error 0: Incorrect params, only 1 param should be given, filename
if len(args) != 1:
    print("Qemu: Error 0: Missing bootloader binary param.\n\tUsage: qemu [bootloader]")
    sys.exit()

filename, = args

# Checks if the given file actually exists
try:
    with open(filename, 'rb') as f:
        contents = f.read().hex()

except FileNotFoundError:
    print("Qemu: Error 1: File '%s' does not exist in the current directory. Check if that file is in the current directory" % filename)
    sys.exit()

# Checks if the first 2 bytes are "RW", to make sure the bootloader is runnable under the EMP32 series CPU instruction set
if contents[:4] != '5257':
    print("Qemu: Error 2: %s is not a valid binary for EMP32 instruction encoding" % filename)

# Putting this after the fact so the pygame message only appears if qemu actually starts
import math
import threading
import time

import pygame

from Hardware import CPU

pygame.init()

# Ratios were all trial and error
FONTSIZE = 11

# Commador 64 Font
font = pygame.font.Font("fonts\\C64_Pro_Mono-STYLE.ttf", FONTSIZE) # 80x50 chars

screen = pygame.display.set_mode((FONTSIZE*80, FONTSIZE*50))
clock = pygame.time.Clock()

cpu = CPU()

# Threads the CPU so the pygame window can update
cpuThread = threading.Thread(target=cpu.Boot, args=[filename])
cpuThread.start()


def blitChar(character: int, color: int, posX: int, posY: int, screen: object):
    '''Writes a character to the screen and the (posX, posY) cordinate position
    
    ```
    blitChar(ord("H"), 0x0F, 0, 0, screen)
    ```
    '''

    background = (((color & 0b01000000)>>6)*255, ((color & 0b00100000)>>5)*255, ((color & 0b00010000)>>4)*255)
    foreground = (((color & 0b0100)>>2)*255, ((color & 0b0010)>>1)*255, (color & 0b0001)*255)

    if character != 0:
        text = font.render(chr(character), True, foreground, background)
        screen.blit(text, (posX*FONTSIZE, posY*FONTSIZE))


run = True

time.sleep(0.5)

while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    posX = 0
    posY = 0

    # Writes characters from video memory onto screen
    i = 0

    while i < (80*50*2):
        char = cpu.Memory[0xb8000 + i: 0xb8000 + i+2]
        blitChar(char[0], char[1], posX, posY, screen)
        posX += 1

        if posX == 80:
            posX = 0
            posY += 1

        i += 2

    # Updates and limits framerate to 30 fps
    pygame.display.update()
    clock.tick(30)

# Exits pygame and turns on signal for the CPU to exit
pygame.quit()
cpu.Shutdown()
