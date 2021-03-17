import sys

here = '\\'.join(__file__.split('\\')[:-3])
bins = here + '\\src\\bin\\'
scripts = here + '\\src\\scripts\\'

sys.path.append(scripts)
sys.path.append(scripts + 'utils\\')

with open(here + '\\settings\\config.conf', 'r') as f:
    for i in f.readlines():
        if i.startswith('monitor-port'):
            port = i.strip('monitor-port').replace(' ', '').replace('\n', '')

port = int(port, 16)
port = '{0:b}'.format(port)
while len(port) < 16:
    port = '0' + port
port += '.bin'

import charmap1

class GPU:
    def __init__(self, window):
        self.window = window
        global port
        self.port = port

    def update(self):
        with open(bins + 'DISK\\' + self.port, 'r') as f:
            lines = f.readlines()
        lines = ''.join(lines).replace(' ', '')
        lines = lines.split('\n')
        letters = {
            '00000000': 'A',
            '00000001': 'B',
            '00000010': 'C',
            '00000011': 'D',
            '00000100': 'E',
            '00000101': 'F',
            '00000110': 'G',
            '00000111': 'H',
            '00001000': 'I',
            '00001001': 'J',
            '00001010': 'K',
            '00001011': 'L',
            '00001100': 'M',
            '00001101': 'N',
            '00001110': 'O',
            '00001111': 'P',
            '00010000': 'Q',
            '00010001': 'R',
            '00010010': 'S',
            '00010011': 'T',
            '00010100': 'U',
            '00010101': 'V',
            '00010110': 'W',
            '00010111': 'X',
            '00011000': 'Y',
            '00011001': 'Z',
            '00011010': 'a',
            '00011011': 'b',
            '00011100': 'c',
            '00011101': 'd',
            '00011110': 'e',
            '00011111': 'f',
            '00100000': 'g',
            '00100001': 'h',
            '00100010': 'i',
            '00100011': 'j',
            '00100100': 'k',
            '00100101': 'l',
            '00100110': 'm',
            '00100111': 'n',
            '00101000': 'o',
            '00101001': 'p',
            '00101010': 'q',
            '00101011': 'r',
            '00101100': 's',
            '00101101': 't',
            '00101110': 'u',
            '00101111': 'v',
            '00110000': 'w',
            '00110001': 'x',
            '00110010': 'y',
            '00110011': 'z',
            '00110100': '0',
            '00110101': '1',
            '00110110': '2',
            '00110111': '3',
            '00111000': '4',
            '00111001': '5',
            '00111010': '6',
            '00111011': '7',
            '00111100': '8',
            '00111101': '9',
            '00111110': '-',
            '00111111': ' ',
            '01000000': '=',
            '01000001': '>',
            '01000010': '.',
            '01000011': '_',
            '01000100': ''
        }
        x = 0
        y = 0
        for i in lines:
            if i.strip('\n') == '':
                continue
            let = charmap1.Char(letters[i[12:]], i[:12], self.window)
            let.draw((x, y))
            x += 20
            if x > 1900:
                x = 0
                y += 20
