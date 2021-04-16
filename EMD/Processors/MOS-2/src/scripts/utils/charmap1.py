import pygame

class Pixel:
    def __init__(self, color, pos):
        self.color = (color[0]*85, color[1]*85, color[2]*85)
        self.pos = pos

    def draw(self, window):
        pass

class Char:
    def __init__(self, letter, color, window):
        self.letter = letter
        color = [int(color[:4], 2), int(color[4:8], 2), int(color[8:12], 2)]
        self.color = (color[0]*8, color[1]*8, color[2]*8)
        self.window = window

    def draw(self, pos):
        font = pygame.font.SysFont('couriernew', 24)
        img = font.render(self.letter, True, self.color)
        self.window.blit(img, pos)
