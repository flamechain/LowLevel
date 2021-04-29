# My FAT32

## Directory Entry (32 Bytes)

| Bytes | Description |
|-|-|
| 1 | First character in filename (0x00 if unallocated) |
| 10 | Last 7 bytes in filename, plus the 3 byte extension |
| 1 | File attributes |
| 8 | File allocation table location (directory table for directories) |
| 4 | Filesize (ignored for directories) |
| 8 | - |
|

### File Attributes

| Bit Position | Description |
|-|-|
| 0000 0001 | Read only |
| 0000 0010 | Hidden file |
| 0000 0100 | System file |
| 0000 1000 | Volume label |
| 0001 0000 | Long file name* |
| 0010 0000 | Directory |
| 0100 0000 | Archive |
| 1000 0000 | - |
|

## FAT Entry (8 Bytes)

| Size | Description |
|-|-|
| 4 Bytes | ID (most significant bit unused) |
| 1 Bit | Allocated (0 for false, 1 for true) |
| 4 Bytes - 1 Bit | Next ID |
|

## Block (32 Bytes)

| Bytes | Description |
|-|-|
| 4 | ID |
| 28 | Data |
|
