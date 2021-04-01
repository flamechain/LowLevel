import pygame
import threading
from CPU import CPU
from Source import Memory

pygame.init()

display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
mem = Memory(0xbFFFF)
cpu = CPU()
cpu.LoadMemory(mem)
run = True

t = threading.Thread(target=cpu.Start)
t.start()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
