import threading

import pygame

from Instructions import *
from Source import Memory
from CPU import CPU

TEXTSIZE = 24
TEXTWIDTH = round(TEXTSIZE*(14/16))
TEXTHEIGHT = round(TEXTSIZE*(18/16))

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
cpu = CPU()
run = True
font = pygame.font.Font('joystix monospace.ttf', TEXTSIZE)
cpu.LoadImage('kernel.iso')
t = threading.Thread(target=cpu.Start, args=[0x400])
t.start()

def WriteChar(char: str, style: int, pos: tuple, display: pygame.display.set_mode):
    background = (((style & 0b0100_0000) >> 6)*255, ((style & 0b0010_0000) >> 5)*255, ((style & 0b0001_0000) >> 4)*255)
    foreground = (((style & 0b0000_0100) >> 2)*255, ((style & 0b0000_0010) >> 1)*255, ((style & 0b0000_0001))*255)
    pygame.draw.rect(display, background, pygame.Rect(pos[0], pos[1], TEXTWIDTH, TEXTHEIGHT))
    text = font.render(char, True, foreground)
    display.blit(text, pos)

while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    counter = 0xb8000
    style = 0
    styled = False

    for i in range(64):
        if not styled:
            style = cpu.Memory[counter]
            styled = True

        else:
            char = cpu.Memory[counter]

            if char != 0:
                WriteChar(chr(char), style, ((i//2)*TEXTWIDTH, -3), screen)
                styled = False

        counter += 1

    pygame.display.update()
    clock.tick(30)

pygame.quit()
cpu.ForceExit()
