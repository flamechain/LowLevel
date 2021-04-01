import sys

# sys.argv[0] is always the current filename, so it can be stripped
args = sys.argv[1:]

# Error 0: Incorrect params, only 1 param should be given, filename
if len(args) != 1:
    print("Qemu: Error 0: Missing bootloader binary param.\n\tUsage: qemu [bootloader]")
    sys.exit()

filename, = args

# Checks if the given file actually exists
try:
    with open(filename, 'rb') as f:
        contents = f.read().hex()

except FileNotFoundError:
    print("Qemu: Error 1: File '%s' does not exist in the current directory. Check if that file is in the current directory" % filename)
    sys.exit()

# Checks if the first 2 bytes are "RW", to make sure the bootloader is runnable under the EMP32 series CPU instruction set
if contents[:4] != '5257':
    print("Qemu: Error 2: %s is not a valid binary for EMP32 instruction encoding" % filename)
