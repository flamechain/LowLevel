'''
Assembles ASM code into machine code using 2 passes
'''

import sys

import termcolor

letters = {
    'H': '01001000',
    'e': '01100101',
    'l': '01101100',
    'o': '01101111',
    ',': '00101100',
    ' ': '00100000',
    'w': '01110111',
    'r': '01110010',
    'd': '01100100',
    '!': '00100001'
}

class Assembler:

    def __init__(self):
        self.errors = []
        self.outfile = 'a.out'
        self.infile = None
        self.errorfile = None
        self.fatal = False
        self.code = []
        self.hexdump = False


    def GetArgs(self):
        '''Gets arguments from sys.argv'''
        try:
            self.infile = sys.argv[1]
            filetype = self.infile.split('.')[1]

            if filetype.lower() != 'asm':
                errors.append('asm: %s: file format not recongnized' % self.infile)

            filename = self.infile.split('.')[0]
            self.errorfile = filename + '.asmerrors'
            args = sys.argv[1:]

            try:
                with open(self.errorfile, 'r') as f:
                    f.read()

            except:
                self.errorfile = None

        except:
            if self.errorfile is not None:
                with open(errorfile, 'a+') as f:
                    f.write('asm: %s no input files' % 'fatal error:')
                    self.fatal = True
                    self.Exit()

            else:
                print('asm: %s no input files' % termcolor.colored('fatal error:', 'red'))
                self.fatal = True
                self.Exit()

        for i in range(len(args)):
            if args[i] == '-o':
                try:
                    self.outfile = str(args[i+1]) + '.bin'

                except:
                    self.errors.append('asm: error: missing filename after \'-o\'')
            
            elif args[i] == '-hexdump':
                self.hexdump = True

        try:
            with open(self.infile, 'r') as f:
                contents = f.read()

        except:
            self.errors.append('asm: %s %s: No such file or directory' % ('error:', self.infile))
            inputfile = None


        if self.errors != []:
            for i in self.errors:
                if self.errorfile is not None:
                    with open(self.errorfile, 'a+') as f:
                        f.write(i)

                else:
                    print(i.replace('error:', termcolor.colored('error:', 'red')))

            if self.infile is None:
                if self.errorfile is not None:
                    with open(self.errorfile, 'a+') as f:
                        f.write('asm: fatal error no input files')
                        self.fatal = True

                else:
                    print('asm: %s no input files' % termcolor.colored('fatal error:', 'red'))
                    self.fatal = True
            self.Exit()

        with open(self.infile, 'r') as f:
            self.code = f.readlines()


    def Exit(self):
        '''Exits compilation'''

        if self.fatal:
            if self.errorfile is not None:
                with open(self.errorfile, 'a+') as f:
                    f.write('compilation terminated.')

            else:
                print('compilation terminated.')

        sys.exit()


    def cleanParts(self, parts, line, amount=2):
        '''Cleans up parts for interpreting'''
        removeparts = []

        if isinstance(parts, str):
            return [parts]

        for i in range(len(parts)):
            if ';' in parts[i]:
                parts[i:] = ''
                break

            elif parts[i].replace(' ', '').strip('\n') == '':
                removeparts.append(i)

        for i in range(len(removeparts)):
            parts.pop(removeparts[i]-i)

        for i in range(len(parts)):
            parts[i] = parts[i].strip('\n')

        if amount is not None:
            if len(parts) != amount:
                if self.errorfile is not None:
                    with open(self.errorfile, 'a') as f:
                        f.write('asm: %s: invalid syntax: \n\t%s' % (self.infile, line))
                        self.Exit()
            
                else:
                    print('asm: %s: invalid syntax: \n\t%s' % (self.infile, line))
                    self.Exit()

        return parts


    def Bin(self, value, length):
        '''Create binary number of n length'''
        value = '{0:b}'.format(int(value))

        return '0'*(length-len(value)) + value


    def trueValue(self, value, variables):
        if value.startswith('$'):
            value = value.strip('$')
            value = '0x' + value
            return int(value, 16)
        elif value.startswith('#$'):
            value = value.strip('#$')
            value = '0x' + value
            return int(value, 16)
        elif value.startswith('#%'):
            value = value.strip('#%')
            value = self.Bin(int(value, 2), 8)
            return int(value, 2)
        elif value.startswith('%'):
            value = value.strip('%')
            value = self.Bin(int(value, 2), 16)
            return int(value, 2)
        elif value.startswith('#'):
            value = value.strip('#')
            if value.startswith('('):
                value = value.strip('()')
                parts = self.cleanParts(value.split(' '), value, amount=3)
                if parts[0] in variables:
                    parts[0] = variables[parts[0]]
                if parts[2] in variables:
                    parts[2] = variables[parts[2]]
                if parts[1] == '|':
                    value = parts[0] | parts[2]
            elif value in variables:
                value = variables[value]
            elif value.startswith('"'):
                value = value.replace('"', '')
                value = letters[value]
                value = int(value, 2)
            value = int(value)
            return value


    def Assemble(self):
        '''Assembles code'''
        blankLines = []

        for i in range(len(self.code)):
            line = self.code[i].split(';')[0]

            if line.replace(' ', '').replace('\t', '').strip('\n') == '':
                blankLines.append(i)

        for i in range(len(blankLines)):
            self.code.pop(blankLines[i]-i)

        variables = {}
        sections = {}
        assembled = []

        address = 0x0

        for i in self.code:
            if '.org' in i:
                line = i.strip('    ')
                parts = self.cleanParts(line.split(' '), i)
                address = self.trueValue(parts[1], variables)
            elif i.endswith(':\n'):
                sections[i.split(':')[0]] = address
            elif '=' in i:
                i = i.replace(' ', '').strip('\n').split('=')
                variables[i[0]] = self.trueValue(i[1], variables)

            else:
                if 'ldac' in i:
                    address += 2
                elif 'stac' in i:
                    address += 3
                elif 'ror' in i:
                    address += 1
                elif 'jmp' in i:
                    address += 3
                elif 'rsr' in i:
                    address += 1
                elif 'jsr' in i:
                    address += 3

        address = 0x0

        for i in range(16**4):
            assembled.append('00000000')

        for i in self.code:
            if not i.startswith('    '):
                if ':' in i:
                    currSection = sections[i.split(':')[0]]

            if i.startswith('    '):
                line = i.strip('    ')

                if line.startswith('nop'):
                    assembled[address] = '00000001'

                elif line.startswith('.'):
                    if '.org' in line:
                        parts = self.cleanParts(line.split(' '), line)
                        address = self.trueValue(parts[1], variables)
                        continue
                    elif '.word' in line:
                        parts = self.cleanParts(line.split(' '), line)
                        if parts[1] in sections:
                            word = sections[parts[1]]
                            word = self.Bin(word, 16)
                            assembled[address] = word[:8]
                            address += 1
                            assembled[address] = word[8:]

                elif line.startswith('ldac'):
                    parts = self.cleanParts(line.split(' '), line, None)
                    if len(parts) == 1:
                        assembled[address] = '11101000'
                    elif parts[1] in variables:
                        byte = variables[parts[1]]
                        assembled[address] = '11101000'
                        byte = self.Bin(byte, 8)
                        address += 1
                        assembled[address] = byte
                    else:
                        byte = self.trueValue(' '.join(parts[1:]), variables)
                        byte = self.Bin(byte, 8)
                        assembled[address] = '11101000'
                        address += 1
                        assembled[address] = byte

                elif line.startswith('stac'):
                    parts = self.cleanParts(line.split(' '), line, None)
                    if len(parts) == 1:
                        assembled[address] = '00110001'
                        address += 1
                        continue
                    assembled[address] = '00110001'
                    if parts[1] in variables:
                        word = variables[parts[1]]
                        word = self.Bin(word, 16)
                    else:
                        word = self.trueValue(parts[1], variables)
                        word = self.Bin(word, 16)
                    address += 1
                    assembled[address] = word[:8]
                    address += 1
                    assembled[address] = word[8:]

                elif line.startswith('jmp'):
                    parts = self.cleanParts(line.split(' '), line)
                    assembled[address] = '11100000'
                    if parts[1] in sections:
                        word = sections[parts[1]]
                        address += 1
                        assembled[address] = self.Bin((word & 0xFF00) >> 8, 8)
                        address += 1
                        assembled[address] = self.Bin(word & 0xFF, 8)

                elif line.startswith('ror'):
                    parts = self.cleanParts(line.split(' '), line, None)
                    if len(parts) == 1:
                        assembled[address] = '00011110'

                elif line.startswith('rsr'):
                    assembled[address] = '00100011'

                elif line.startswith('jsr'):
                    parts = self.cleanParts(line.split(' '), line)
                    assembled[address] = '11100010'
                    if parts[1] in sections:
                        word = sections[parts[1]]
                        address += 1
                        assembled[address] = self.Bin((word & 0xFF00) >> 8, 8)
                        address += 1
                        assembled[address] = self.Bin(word & 0xFF, 8)

                else:
                    if self.errorfile is not None:
                        with open(self.errorfile, 'a') as f:
                            f.write('asm: %s: invalid syntax: \n\t%s' % (self.infile, line))
                            self.Exit()
                    
                    else:
                        print('asm: %s: invalid syntax: \n\t%s' % (self.infile, line))
                        self.Exit()
                
                address += 1

        return assembled


    def Finish(self, code) -> None:
        '''Finishes Assembler'''
        with open(self.outfile, 'w') as f:
            f.writelines(code)
        
        address = 0x0
        first = True
        count = 0
        inarow = True
        if self.hexdump:
            print('Hex:', end='')
            for i in code:
                if (count > 5) and inarow:
                    count = 0
                    first = True
                if (int(i, 2) != 0) or (first == False):
                    if int(i, 2) == 0:
                        count += 1
                        inarow = True
                    else:
                        inarow = False
                        count = 0
                    if first:
                        print('\n' + hex(address), end=': ')
                        first = False
                    print(hex(int(i, 2)), end=' ')

                address += 1


asm = Assembler()
asm.GetArgs()

# For Debugging:
# asm.infile = 'Assembler/testing.asm'
# with open(asm.infile, 'r') as f:
#     asm.code = f.readlines()

code = asm.Assemble()
asm.Finish(code)

with open(asm.outfile, 'w') as f:
    f.writelines(code)
