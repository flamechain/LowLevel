# README

## Linux and Mac

```bash
make
qemu dist/x86_64/kernel.iso
```

## Windows

```bash
docker build buildenv -t cos.0.5-buildenv
docker run --rm -it -v %cd%:/root/env cos.0.5-buildenv
make
qemu-system-x86_64 dist/x86_64/kernel.iso
```
