import re

def main(outfile, infile):
    with open('build\\' + infile, 'rb') as f:
        contents = f.read().hex()
        contents = re.findall('..', contents)

    entry = int(contents[0], 16) << 24 | int(contents[1], 16) << 16 | int(contents[2], 16) << 8 | int(contents[3], 16)
    contents = contents[3:]
    iso = bytearray()
    iso.extend(bytes([0xC]))
    iso.extend(bytes([0b011]))
    iso.extend(bytes([0b0111]))
    iso.extend(bytes([0x0]))
    iso.extend(bytes([0x10]))
    iso.extend(bytes([1]))
    iso.extend(bytes([0b110]))
    iso.extend(bytes([(entry & 0xFF00) >> 8]))
    iso.extend(bytes([entry & 0xFF]))
    iso.extend(bytes([0]))
    iso.extend(bytes([0xF]))
    iso.extend(bytes([0]))
    iso.extend(bytes([0]))
    iso.extend(bytes([0]))
    iso.extend(bytes([0]))

    for i in contents:
        iso.extend(bytes([int(i, 16)]))

    with open('dist\\' + outfile + '.iso', 'wb') as f:
        f.write(iso)

if __name__ == "__main__":
    import sys
    infile = sys.argv[1]
    outfile = sys.argv[3]
    main(outfile, infile)
