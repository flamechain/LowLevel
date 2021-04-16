import sys
import termcolor
import re

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
    '00111111': ' '
}

class result:
    def __init__(self, content, type):
        self.content = content
        self.type = type

class main:
    registers = {
        'FLAGS': '00000',
        'eax': '00001',
        'ebx': '00010',
        'ecx': '00011',
        'edx': '00100',
        'eex': '00101',
        'efx': '00110',
        'fax': '00111',
        'fbx': '01000',
        'fcx': '01001',
        'fdx': '01010',
        'fex': '01011',
        'ffx': '01100'
    }

    variables = {

    }

    gotos = {
        '.start': '0000000000000000'
    }

    scheduled = {
        
    }

    def __init__(self, code):
        self.code = code
        self.curr = None
        self.bin = []

    def createData(self, value, length=16):
        while len(value) < length:
            value = '0' + value
        return value

    def createType(self, type, value):
        struct = ''
        if type == 'uint':
            struct += '000'
            value = '{0:b}'.format(int(value))
            value = self.createData(value)
            struct += value
        elif type == 'int':
            struct += '010'
            if int(value) < 0:
                struct += '1'
            else:
                struct += '0'
            value = value[1:]
            value = '{0:b}'.format(int(value))
            value = self.createData(value, 15)
            struct += value
        return struct

    def Compile(self, name='a'):
        toremove = []
        self.code = self.code.split('\n')
        for i in range(len(self.code)):
            if self.code[i].replace(' ', '').replace('\n', '').replace('\t', '') == '':
                toremove.append(i)
        for i in range(len(toremove)):
            self.code.pop(toremove[i]-i)
        struct = ''

        self.bin.append('100010 000000 000000 000000')

        addr = 0
        for i in self.code:   
            if i.startswith('.'):
                self.gotos[i] = self.createData('{0:b}'.format(addr))
                self.scheduled[addr] = '00110100000000000000000000000000'
            addr += 1

        addr = 0
        for i in self.code:
            if i.startswith('SET '):
                struct = '011000'
                parts = i.strip('SET ').replace(' ', '').split('//')[0].split(',')
                struct += self.registers[parts[0]]
                var = parts[1]
                if var.startswith('uint'):
                    vartype = 'uint'
                elif var.startswith('int'):
                    vartype = 'int'
                varvalue = var.strip(vartype)
                var = self.createType(vartype, varvalue)
                struct += var + '00'
            elif i.startswith('ADD '):
                struct = '000000'
                parts = i.strip('ADD ').replace(' ', '').split('//')[0]
                parts = re.split(',|->', parts)
                struct += self.registers[parts[0]] + self.registers[parts[1]] + self.registers[parts[2]] + '00000000000'
            elif i.startswith('MOV '):
                struct = '001100'
                parts = i.strip('MOV ').replace(' ', '').split('//')[0].split('->')
                struct += self.registers[parts[0]] + self.registers[parts[1]]
                struct += '0000000000000000'
            elif i.startswith('INMT '):
                struct = '011111'
                parts = i.strip('INMT ').replace(' ', '').split('//')[0]
                struct += self.registers[parts]
                struct += '000000000000000000000'
            elif i.startswith('JMP '):
                struct = '001000'
                parts = i.strip('JMP ').replace(' ', '').split('//')[0]
                struct += self.gotos[parts]
                struct += '0000000000'
            elif i.startswith('HLT'):
                struct = '01000100000000000000000000000000'
            elif i.startswith('Jcc '):
                struct = '001001'
                parts = i.strip('Jcc ').replace(' ', '').split('//')[0].split(',')
                struct += self.variables[parts[0]]
                struct += self.gotos[parts[1]]
            elif '=' in i:
                struct = '001010'
                parts = i.replace(' ', '').split('//')[0].split('=')
                self.variables[parts[0]] = self.createData('{0:b}'.format(addr), length=10)
                parts = parts[1].strip('CMP').split(',')
                struct += self.registers[parts[0]] + self.registers[parts[1]]
                struct += '0000000000000000'
            elif i.startswith('//'):
                continue
            elif i.startswith('.'):
                for i in self.scheduled:
                    if addr == i:
                        struct = self.scheduled[i]
            elif i.startswith('EXIT'):
                struct = '011010'
                struct += '00000000000000000000000000'
            elif i.startswith('LOOP '):
                struct = '100001'
                parts = i.strip('LOOP ').replace(' ', '').split('//')[0].split('->')
                struct += self.registers[parts[0]] + self.gotos[parts[1]]
                struct += '00000'
            else:
                text = termcolor.colored('compile error:', 'red')
                command = "'" + i.split(' ')[0] + "'"
                print('masm.exe: %s unknown instruction %s' % (text, command))
                sys.exit()

            self.bin.append(struct)
            addr += 1
            struct = ''
        while len(self.bin) < 16:
            self.bin.append('01101000000000000000000000000000')
        self.bin.append('')
        return '\n'.join(self.bin)

def compiler(infile, path=None):
    code = ''
    try:
        with open(infile, 'r') as f:
            code = f.read()
    except:
        try:
            with open(path + infile, 'r') as f:
                code = f.read()
        except:
            try:
                with open(path + '\\' + infile, 'r') as f:
                    code = f.read()
            except:
                return result('file does not exist', 'error')

    res = main(code).Compile()
    return result(res, 'bin')

if len(sys.argv) < 2:
    text = termcolor.colored('fatal error:', 'red')
    print('masm.exe: %s no input files' % text)
    sys.exit()
else:
    FILE = sys.argv[1]
    ARGS = sys.argv[1:]
    if FILE.endswith('.masm'):
        pass
    else:
        text = termcolor.colored('fatal error:', 'red')
        print('masm.exe: %s invalid file type' % text)
        sys.exit()

outfile = 'a'
diskfile = None

for i in range(len(ARGS)):
    if ARGS[i] == '-o':
        outfile = ARGS[i+1]
    elif ARGS[i] == '-d':
        diskfile = outfile

here = '\\'.join(__file__.split('\\')[:-1]) + '\\'
sys.path.append(here)

out = compiler(FILE, here)

if out.type == 'error':
    text = termcolor.colored('compile error:', 'red')
    print('masm.exe: %s %s' % (text, out.content))
elif out.type == 'bin':
    if diskfile is None:
        with open(here + outfile + '.bin', 'w') as f:
            f.write(out.content)
    else:
        with open('\\'.join(__file__.split('\\')[:-3]) + '\\' + outfile + '.bin', 'w') as f:
            f.write(out.content)
