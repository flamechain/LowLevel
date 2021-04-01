# Running

## Docker Container

To build the docker container:

```cmd
docker build [Dockerfile folder] -t [Tag name]

e.g.

docker build buildenv -t myos-buildenv
```

To run the docker container:

```cmd
docker run --rm -it -v %cd%:[Specified workdir] [Tag name]

e.g.

docker run --rm -it -v %cd%:/root/env myos-buildenv
```

## NASM and QEMU

To assemble:

```cmd
nasm -f bin [filename] -o [filename].bin

e.g.

nasm -f bin boot.asm -o boot.bin
```

Or you can run a makefile:

```cmd
make [makefile command]

e.g.

make build
```

To run the emulator:

```cmd
qemu [imagename]

e.g.

qemu boot.bin

You make have to use qemu-system-x86_64 instead of qemu
```
