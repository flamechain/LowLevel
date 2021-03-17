import re
import argparse

def Assemble(code):
    pass

def main(argv):
    with open(argv.i, 'r') as f:
        lines = f.read().split('\n')

    binary = Assemble(lines)
    outfile = 'a.o'

    try:
        outfile = argv.o
    except: pass

    with open(outfile, 'wb') as f:
        f.write(binary)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('i', help="Input file to assemble")
    parse.add_argument('-o', help="Outfile file to put result, automatically converts to *.bin")
    # parse.add_argument('-d', help="Debug level, for debugging only", type=int)
    args = parse.parse_args()

    main(args)
