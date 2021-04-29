def DirectoryEntry(filename: str, fileattr: int, filecontents: str) -> bytes:
    entry = [ord(i) for i in filename]
    entry.append(fileattr)
    loc = 1
    entry.extend([0, 0, 0, 0, 0, 0, 0, loc])
    loc += 1
    filelen = [(len(filecontents)&0xFF000000)>>24,(len(filecontents)&0xFF0000)>>16,(len(filecontents)&0xFF00)>>8,len(filecontents)&0xFF]
    entry.extend(filelen)
    entry.extend([0]*8)
    for i in range(len(filecontents) // 28):
        content = [ord(i) for i in filecontents[i*28:(i+1)*28]]
        content.extend([(loc&0xFF000000)>>24,(loc&0xFF0000)>>16,(loc&0xFF00)>>8,loc&0xFF])
        entry.extend(bytes(content))
        loc += 1
    return entry

with open('mem.bin', 'wb') as f:
    f.write(bytes([0]*32))

_file = \
'''
This is my file contents.
Im making this over 28 characters so that is takes up more than 1 block and I can test blocking.
'''

mem = bytearray()
entry = DirectoryEntry('myfile  txt', 0b00000000, _file)
mem.extend(bytes(entry))

with open('mem.bin', 'wb') as f:
    f.write(mem)

with open('mem.bin', 'rb') as f:
    contents = f.read()

disk = []
for i in range(len(contents)//32):
    disk.append(''.join([chr(i) for i in contents[i*32:(i+1)*32]]))

print(disk)
