'''
LCD Pygame Window
'''

import sys
import threading
import time

letters = {
    '01001000': 'H',
    '01100101': 'e',
    '01101100': 'l',
    '01101111': 'o',
    '00101100': ',',
    '00100000': ' ',
    '01110111': 'w',
    '01110010': 'r',
    '01100100': 'd',
    '00100001': '!'
}

class LCD:
    def __init__(self, window, pygame):
        pygame.display.set_caption('LCD Display')
        img = pygame.image.load('icon.png')
        pygame.display.set_icon(img)
        self.window = window
        self.input = 0b00000000000
        self.on = False
        self.output = None
        self.clock = 0
        self.run = False

    def Start(self, pygame):
        self.run = True
        self.Execute(pygame)

    INS_CLEAR   = 0b0000000001
    INS_RETURN  = 0b0000000010
    INS_ENTRY   = 0b0000000100
    INS_DISPLAY = 0b0000001000
    INS_CURSOR  = 0b0000010000
    INS_FUNC    = 0b0000100000
    INS_CADDR   = 0b0001000000
    INS_DADDR   = 0b1000000000
    INS_READ    = 0b0100000000

    def Execute(self, pygame):

        cursor = False
        blink = False
        display = False
        increment = False
        shift = False
        pos = [0, 0]

        displayed_letters = []
        font = pygame.font.SysFont('couriernew', 30)

        while self.run:
            if self.clock > 0:
                if (self.input & 0b10000000000) > 0:
                    Ins = self.input - 1024

                    if Ins & self.INS_READ > 0:
                        pass

                    elif Ins & self.INS_DADDR > 0:
                        if Ins & 0b1000000000 > 0:
                            binary = self.input & 0b0011111111
                            binary = '{0:b}'.format(binary)
                            binary = '0'*(8-len(binary)) + binary
                            letter = letters[binary]
                            img = font.render(letter, True, (255, 255, 255))
                            if cursor:
                                displayed_letters.append(img)
                                self.window.fill((20, 20, 20))
                                if increment:
                                    pos = [5, 0]
                                else:
                                    pos = [180, 0]
                                for i in displayed_letters:
                                    self.window.blit(i, pos)
                                    if increment:
                                        pos[0] += 20
                                    else:
                                        pos[0] -= 20
                                cursor_letter = font.render('_', True, (255, 255, 255))
                                self.window.blit(cursor_letter, [pos[0], pos[1] - 5])
                            else:
                                self.window.blit(img, pos)
                                if increment:
                                    pos[0] += 20
                                else:
                                    pos[0] -= 20

                    elif Ins & self.INS_CADDR > 0:
                        pass

                    elif Ins & self.INS_FUNC > 0:
                        pass

                    elif Ins & self.INS_CURSOR > 0:
                        pass

                    elif Ins & self.INS_DISPLAY > 0:
                        display = True if (Ins & 0b100) > 0 else False
                        cursor  = True if (Ins & 0b010) > 0 else False
                        blink   = True if (Ins & 0b001) > 0 else False
                        if display:
                            self.window.fill((20, 20, 20))

                    elif Ins & self.INS_ENTRY > 0:
                        increment = True if (Ins & 0b10) > 0 else False
                        shift = True if (Ins & 0b1) > 0 else False
                        if increment:
                            pos = [5, 0]
                        else:
                            pos = [180, 0]

                    elif Ins & self.INS_RETURN > 0:
                        pass

                    elif Ins & self.INS_CLEAR > 0:
                        displayed_letters = []
                        self.window.fill((20, 20, 20))

                self.clock -= 1
