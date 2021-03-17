import re
import sys
import termcolor

def main(argv: list):
    '''Function wraps Convert program'''

    error = termcolor.colored("error:", "red")
    mode = "bin"
    op = "a.out"

    # Checks filename
    if not argv[0].endswith("Convert.py"):
        return print("Convert: incorrect file name '%s'" % argv[0])

    # Checks argv length
    if len(argv) < 2:
        return print("Convert: %s no input files, try:\n    $ python Convert.py <filename> <args>" % error)

    # Checks input file
    fp = argv[1]

    try:
        with open(fp, "r") as f:
            f.read()

    except:
        return print("Convert: %s file '%s' does not exist" % (error, fp))

    # Checks args
    i = 2
    while i < len(argv):
        arg = argv[i]

        if arg.startswith('-'):
            if arg == "-d":
                mode = 'd'
            elif arg == "-o":
                try:
                    op = argv[i+1]
                except:
                    return print("Convert: %s no outfile given after '-o'" % error)

            else:
                return print("Convert: %s unknown argument '%s'" % (error, arg))

        i += 1

    if mode == 'd':
        with open(fp, "r") as f:
            contents = f.read().replace(' ', '').replace('\n', '')
            array = bytearray()
            for i in re.findall("........", contents):
                array.extend(bytes([int(i, 2)]))
        
        if op == "out":
            print(array)
        else:
            with open(op, "wb") as f:
                f.write(array)

    elif mode == "bin":
        with open(fp, "rb") as f:
            contents = f.read()
            contents = re.findall("..", contents.hex())
            newcontents = ''

            for i in contents:
                strn = '{0:b}'.format(int(i, 16))
                newcontents += '0'* (8-len(strn)) + strn
            
        if op == "out":
            print(newcontents)

        else:
            with open(op, "w") as f:
                f.write(newcontents)


if __name__ == "__main__":
    args = sys.argv

    main(args)
