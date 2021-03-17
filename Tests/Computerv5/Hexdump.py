import sys
import termcolor
import re


def main(argv: list):
    '''Function wraps hexdump program'''

    error = termcolor.colored("error:", "red")
    mode = "bin"
    style = "s2"
    color = False

    # Checks filename
    if not argv[0].endswith("Hexdump.py"):
        return print("Hexdump: incorrect file name '%s'" % argv[0])

    # Checks argv length
    if len(argv) < 2:
        return print("Hexdump: %s no input files, try:\n    $ python Hexdump.py <filename> <args>" % error)

    # Checks input file
    fp = argv[1]

    if fp == "test":
        main(argv=["Hexdump.py", "zeros.bin", "-d"])
        main(argv=["Hexdump.py", "allchars.bin", "-s1", "-d", "-c"])
        return

    try:
        with open(fp, "rb") as f:
            f.read()

    except:
        return print("Hexdump: %s file '%s' does not exist" % (error, fp))

    # Checks args
    i = 2
    while i < len(argv):
        arg = argv[i]

        if arg.startswith('-'):
            if arg == "-d":
                mode = 'd'
            elif arg == "-s1":
                style = "s1"
            elif arg == "-s2":
                style = "s2"
            elif arg == "-c":
                color = True

            else:
                return print("Hexdump: %s unknown argument '%s'" % (error, arg))

        i += 1

    if mode in ['d', "bin"]:
        hexdump = []

        if style == "s1":
            hexdump.append("\nAddress"+termcolor.colored("      00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F","grey" if color else "white")+'   DECODED TEXT\n'+'-'*11+' '+'-'*49+' '+'-'*16+'\n')

    if mode == 'd':
        with open(fp, "r") as f:
            contents = f.read().replace(' ', '').replace('\n', '')

    elif mode == "bin":
        with open(fp, "rb") as f:
            contents = f.read()
            contents = re.findall("..", contents.hex())
            newcontents = ''

            for i in contents:
                strn = '{0:b}'.format(int(i, 16))
                newcontents += '0'* (8-len(strn)) + strn
            
            contents = newcontents
        
    contents = re.findall("........", contents)

    address = 0x00000000
    counter = 0
    decoded = ''
    prevline = ''
    stared = False
    line = ''
    if color:
        color = "grey"
    if (style == "s2") or not color:
        color = "white"

    for i in contents:
        if counter > 15:
            counter = 0

            if prevline == line:
                if not stared:
                    hexdump.append('*\n')
                    stared = True

            else:
                stared = False
                wholeline = termcolor.colored("0x"+'0'*(8-len(hex(address)[2:]))+hex(address)[2:].upper(),color)+' | '+line+'|%s|\n' % decoded

                if style == "s2":
                    wholeline = '0'*(8-len(hex(address)[2:]))+hex(address)[2:]+'  '+line+' |%s|\n' % decoded

                hexdump.append(wholeline)

            prevline = line
            line = ''
            address += 16
            decoded = ''

        dec = chr(int(i,2))

        if (dec < '\x21') or ((dec > '\x7E') and (dec < '\xA1')):
            char = termcolor.colored('.', color)

            if style == "s2":
                char = '.'

            decoded += char

        else:
            decoded += dec

        i = '0'*(2-len(hex(int(i,2))[2:]))+hex(int(i,2))[2:]
        line += i + ' '
        counter += 1

    if line == prevline:
        addr = termcolor.colored("0x"+'0'*(8-len(hex(address)[2:]))+hex(address)[2:].upper(),color)

        if style == "s2":
            addr ='0'*(8-len(hex(address)[2:]))+hex(address)[2:]

        hexdump.append(addr)
    else:
        counter += 1
        const = 17

        if counter > 16:
            const -= 1

        addr = termcolor.colored("0x"+'0'*(8-len(hex(address)[2:]))+hex(address)[2:].upper(),color) + " | "
        const2 = 0

        if style == "s2":
            addr = '0'*(8-len(hex(address)[2:]))+hex(address)[2:] + "  "
            const2 = 1

        hexdump.append(addr+line+"   "*(const-counter)+' '*const2+'|'+decoded+' '*(const-counter)+"|")

    print(''.join(hexdump))


if __name__ == "__main__":
    args = sys.argv
    # use 'test' as <filename> for a test, for example:
    # args = ["Hexdump.py", "test"]

    main(args)
