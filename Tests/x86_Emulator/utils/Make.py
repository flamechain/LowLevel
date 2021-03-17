import termcolor
import sys
import re

sys.path.append('\\'.join(__file__.split('\\')[:-1]))
sys.path.append('\\'.join(__file__.split('\\')[:-1]) + '\\utils\\')
sys.path.append('\\'.join(__file__.split('\\')[:-2]))

import Asm
import Convert
import CPU
import VirtualRAM


def main() -> print or None:
    '''Parses makefile and executes'''

    error = termcolor.colored("error:", "red")

    try:
        with open("makefile", "r") as f:
            contents = f.read()

    except:
        return print("Make: %s couldn't file makefile in directory" % error)

    instruction = False
    infile = None
    outfile = None

    for i in contents.split('\n'):
        if i == '':
            continue

        if i.startswith('\t'):
            if not instruction:
                return print("Make: %s invalid syntax: unexpected indent\n  ->%s" % (error, i))

            if i.strip('\t').startswith("asm"):
                Asm.main(['', infile, "-o", outfile])
            elif i.strip('\t').startswith("convert"):
                Convert.main(['Convert.py', infile, "-o", outfile, "-d"])
            elif i.strip('\t').startswith("Mx86"):
                if outfile == 'stdout':
                    mem = VirtualRAM.Memory()
                    cpu = CPU.CPU(mem)

                    with open(infile, 'rb') as f:
                        contents = f.read()
                        contents = re.findall("..", contents.hex())

                    cpu.LoadProgram(contents)
                    cpu.Execute(80)

        else:
            instruction = True
            line = i.strip('\n').replace(' ', '').split(':')
            infile = line[1]
            outfile = line[0]

    return


if __name__ == "__main__":
    main()
