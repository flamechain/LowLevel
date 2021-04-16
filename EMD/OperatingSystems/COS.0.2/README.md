# COS.0.2

COS.0.2 OS from scratch.

## Build

```cmd
MINGW64 ~/COS.0.2
$ docker build Docker -t cos.0.2-buildenv

MINGW64 ~/COS.0.2
$ docker run --rm -it -v %cd%:/root/env cos.0.2-buildenv
~root/env# nasm -f bin boot.asm -o boot.bin

~root/env# exit

MINGW64 ~/COS.0.2
$ qemu-system-x86_64 boot.bin
```
