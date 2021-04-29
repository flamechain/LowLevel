# OS

## Create

```bash
docker build buildenv -t cos.0.3-buildenv
docker run --rm -it -v %cd%:/root/env cos.0.3-buildenv
docker run --rm -it -v $pwd:/root/env cos.0.3-buildenv
```

## Build

```bash
make clean # may give error
make iso

qemu-system-i386 -drive format=raw,file=boot.iso -d cpu_reset -monitor stdio -device sb16 -audiodev coreaudio,id=coreaudio,out.frequency=48000,out.channels=2,out.format=s32
```
